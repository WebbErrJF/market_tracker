import time
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .models import SubscribedCompanies
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.apps import apps
import json
from .serializers import StockCompanySerializer, InitialDataSerializer
from api_fetcher.models import StockCompany, StockData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.views import View
from datetime import datetime, timedelta


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')


class DashboardView(View):
    template_name = 'users/dashboard.html'

    def get(self, request, *args, **kwargs):
        context = {'title': 'Dashboard'}
        return render(request, self.template_name, context)


class StockListView(View):
    template_name = 'users/stock_list.html'

    def get(self, request, *args, **kwargs):
        context = {'title': 'Stock list data'}
        return render(request, self.template_name, context)


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm()
        profile_form = ProfileUpdateForm()
        context = {'title': 'User profile', 'user_form': user_form, 'profile_form': profile_form}
        return render(request, self.template_name, context)


class StreamView(View):
    @staticmethod
    def __retrieve_data(user_stock_symbols, stock_data_model):
        output = {}
        for user_stock_set in user_stock_symbols:
            stock_object = stock_data_model.objects.select_related('Stock_symbol').filter(
                Stock_symbol__Symbol=user_stock_set[0]).last()
            output[user_stock_set[1]] = {'Data': stock_object}
        return output

    @staticmethod
    def __modify_date(stock_object_dict):
        for stock_object in stock_object_dict.values():
            date_object = stock_object['Data'].stockdate_set.first()
            stock_object['Date'] = date_object.Date.strftime('%Y-%m-%d %H:%M:%S') if stock_object else None

    @staticmethod
    def __generate_output_dict(stock_data):
        output_json = {}
        for key, value in stock_data.items():
            output_json[key] = {'data': value['Data'].Price,
                                'change_point': value['Data'].Change_point,
                                'stock_date': value['Date']
                                }
        return output_json

    def event_stream(self):
        while True:
            time.sleep(30)
            user_stock_symbols = SubscribedCompanies.objects.filter(user__username='jakub', dashboard_number__gt=0
                                                                    ).values_list('stock_company__Symbol',
                                                                                  'dashboard_number', flat=False)
            stock_data_model = apps.get_model('api_fetcher', 'StockData')
            stock_data = self.__retrieve_data(user_stock_symbols, stock_data_model)
            self.__modify_date(stock_data)
            output_dict = self.__generate_output_dict(stock_data)
            data_json = json.dumps(output_dict)
            yield f'data: {data_json}\n\n'

    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(self.event_stream(), content_type='text/event-stream')


class GetAllStockCompanies(APIView):
    def __init__(self):
        self._get_decision_dict = {'all': self.__get_all_stock_companies,
                                   'subscribed': self.__get_subscribed_stock_companies,
                                   'initial': self.__get_initial_stock_data
                                   }
        self._post_decision_dict = {'subscribe': self.__post_subscribed_company,
                                    'display': self.__post_display_company}
        super().__init__()

    def get(self, request, param):
        user = request.user
        response = self._get_decision_dict[param](user)
        return response

    @staticmethod
    def __get_all_stock_companies(user):
        stock_companies = StockCompany.objects.all()
        data = []
        for company in stock_companies:
            subscribed_data = SubscribedCompanies.objects.filter(user=user, stock_company=company)
            serialized_company = StockCompanySerializer(company).data
            if subscribed_data.exists():
                subscription_date = subscribed_data.first().subscription_date
                serialized_company['subscription_date'] = subscription_date
            data.append(serialized_company)
        return Response(data)

    @staticmethod
    def __get_subscribed_stock_companies(user):
        subscribed_companies = SubscribedCompanies.objects.filter(user=user).values('stock_company__Name',
                                                                                    'stock_company__Symbol',
                                                                                    'dashboard_number')
        return Response(subscribed_companies)

    @staticmethod
    def __get_initial_stock_data(user):
        data = []
        subscribed_companies = SubscribedCompanies.objects.filter(user=user, dashboard_number__gt=0).values_list(
            'stock_company__Symbol', 'dashboard_number', flat=False)
        one_day_ago = datetime.now() - timedelta(hours=1)
        for company_symbol, dashboard_number in subscribed_companies:
            stock_data = StockData.objects.filter(Stock_symbol__Symbol=company_symbol, stockdate__Date__gte=one_day_ago)
            serialized_company_data = []
            for data_item in stock_data:
                serialized_data_item = InitialDataSerializer(data_item).data
                date_item = data_item.stockdate_set.first()
                serialized_company_data.append({
                    'data': serialized_data_item,
                    'date': date_item.Date.strftime('%Y-%m-%d %H:%M:%S') if date_item else None
                })
            data.append({
                'symbol': dashboard_number,
                'data': serialized_company_data,
            })
        return Response(data)

    def post(self, request, param):
        user = request.user
        response = self._post_decision_dict[param](request, user)
        return response

    @staticmethod
    def __post_subscribed_company(request, user, *args, **kwargs):
        stock_company_id = request.data.get('stock_company_id')
        stock_company = StockCompany.objects.get(Name=stock_company_id)
        subscribed_entry = SubscribedCompanies.objects.filter(user=user, stock_company=stock_company).first()
        if subscribed_entry:
            subscribed_entry.delete()
            return Response({'message': 'Subscription removed successfully'}, status=status.HTTP_204_NO_CONTENT)
        subscribed_entry, created = SubscribedCompanies.objects.get_or_create(
            user=user, stock_company=stock_company)
        if created:
            subscribed_entry.subscription_date = timezone.now()
            subscribed_entry.save()
            return Response({'message': 'Subscribed successfully'}, status=status.HTTP_201_CREATED)

    @staticmethod
    def __post_display_company(request, user):
        stock_company_symbol = request.data.get('stock_company_symbol')
        dashboard_number = request.data.get('dashboard_number')
        subscribed_company_before = SubscribedCompanies.objects.get(user=user, dashboard_number=dashboard_number)
        subscribed_company_actual = SubscribedCompanies.objects.get(user=user,
                                                                    stock_company__Symbol=stock_company_symbol)
        subscribed_company_before.dashboard_number = 0
        subscribed_company_before.save()
        subscribed_company_actual.dashboard_number = dashboard_number
        subscribed_company_actual.save()
        return Response({'message': 'Post successfully'}, status=status.HTTP_201_CREATED)
