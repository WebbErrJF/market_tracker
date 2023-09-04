async function fetchApiResponse(url) {
      const response = await fetch(url);
      return await response.json();
      }

function createInitialDataTables() {
      const f_chart_init_data = anychart.data.table("date");
      const s_chart_init_data = anychart.data.table("date");
      const t_chart_init_data = anychart.data.table("date");
      const fo_chart_init_data = anychart.data.table("date");
      return {
        1: f_chart_init_data,
        2: s_chart_init_data,
        3: t_chart_init_data,
        4: fo_chart_init_data
      };
      }

function processApiResponse(apiResponse) {
      const initial_data = createInitialDataTables();

      apiResponse.forEach(responseItem => {
        const symbol = responseItem.symbol;
        const dataItems = responseItem.data;

        if (dataItems) {
          dataItems.forEach(dataItem => {
            const price = dataItem.data.Price;
            const open = price + dataItem.data.Change_point;
            const high = open >= price ? open : price;
            const low = open >= price ? price : open;
            const dateItem = dataItem.date;
            initial_data[symbol].addData([
              {"date": dateItem, "open": open, "high": high, "low": low, "close": price}
            ]);
          });
        }
      });

      return initial_data;
    }

function setupCharts(initial_data) {
      TrendMapping1 = initial_data[1].mapAs({value: "close"});
      columnMapping1 = initial_data[1].mapAs({value: "high"});
      ohlcMapping1 = initial_data[1].mapAs({open: "open", high: "high", low: "low", close: "close"});
      TrendMapping2 = initial_data[2].mapAs({value: "close"});
      columnMapping2 = initial_data[2].mapAs({value: "high"});
      ohlcMapping2 = initial_data[2].mapAs({open: "open", high: "high", low: "low", close: "close"});
      TrendMapping3 = initial_data[3].mapAs({value: "close"});
      columnMapping3 = initial_data[3].mapAs({value: "high"});
      ohlcMapping3 = initial_data[3].mapAs({open: "open", high: "high", low: "low", close: "close"});
      TrendMapping4 = initial_data[4].mapAs({value: "close"});
      columnMapping4 = initial_data[4].mapAs({value: "high"});
      ohlcMapping4 = initial_data[4].mapAs({open: "open", high: "high", low: "low", close: "close"});

      chart1 = anychart.stock();
      chart2 = anychart.stock();
      chart3 = anychart.stock();
      chart4 = anychart.stock();

      var line1 = chart1.plot(0);
      line1.area(TrendMapping1).name('Trend');
      var line2 = chart2.plot(0);
      line2.area(TrendMapping2).name('Trend');
      var line3 = chart3.plot(0);
      line3.area(TrendMapping3).name('Trend');
      var line4 = chart4.plot(0);
      line4.area(TrendMapping4).name('Trend');

      chart1.top(25);
      chart1.title("AnyStock Legend: Basic Sample");
      chart2.top(25);
      chart2.title("AnyStock Legend: Basic Sample");
      chart3.top(25);
      chart3.title("AnyStock Legend: Basic Sample");
      chart4.top(25);
      chart4.title("AnyStock Legend: Basic Sample");

      var rangePicker1 = anychart.ui.rangePicker();
      var rangeSelector1 = anychart.ui.rangeSelector();
      var rangePicker2 = anychart.ui.rangePicker();
      var rangeSelector2 = anychart.ui.rangeSelector();
      var rangePicker3 = anychart.ui.rangePicker();
      var rangeSelector3 = anychart.ui.rangeSelector();
      var rangePicker4 = anychart.ui.rangePicker();
      var rangeSelector4 = anychart.ui.rangeSelector();

      var customRanges = [
          {
              'text': '5 Days',
              'type': 'unit',
              'unit': 'day',
              'count': 5,
              'anchor': 'first-visible-date'
          },
          {
              'text': 'Year 2007',
              'startDate': '2007 Jan 1',
              'endDate': '2007 Dec 31',
              'type': 'range'
          },
          {
              'text': 'Full Range',
              'type': 'max'
          },
          {
              'text': '10',
              'type': 'points',
              'count': 10,
              'anchor': 'last-date'
          }
      ];

      rangePicker1.format('dd MM yyyy');
      rangePicker2.format('dd MM yyyy');
      rangePicker3.format('dd MM yyyy');
      rangePicker4.format('dd MM yyyy');

      rangeSelector1.ranges(customRanges);
      rangeSelector1.render(chart1);
      rangeSelector2.ranges(customRanges);
      rangeSelector2.render(chart2);
      rangeSelector3.ranges(customRanges);
      rangeSelector3.render(chart3);
      rangeSelector4.ranges(customRanges);
      rangeSelector4.render(chart4);

      const stage1 = anychart.graphics.create("container");
      const stage2 = anychart.graphics.create("container2");
      const stage3 = anychart.graphics.create("container3");
      const stage4 = anychart.graphics.create("container4");

      chart1.container(stage1);
      chart1.draw();
      chart2.container(stage2);
      chart2.draw();
      chart3.container(stage3);
      chart3.draw();
      chart4.container(stage4);
      chart4.draw();

      chart1.selectRange("ytd");
      rangePicker1.render(chart1);
      chart2.selectRange("ytd");
      rangePicker2.render(chart2);
      chart3.selectRange("ytd");
      rangePicker3.render(chart3);
      chart4.selectRange("ytd");
      rangePicker4.render(chart4);
    }

document.addEventListener('DOMContentLoaded', async function () {
  const apiResponse = await fetchApiResponse(`/subscriptions/${'initial'}`);
  initial_data = processApiResponse(apiResponse);
  setupCharts(initial_data);
});


if(typeof(EventSource) !== "undefined") {
    var source = new EventSource("/stream/");
    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        Object.keys(data).forEach(stockSymbol => {
            const stockInfo = data[stockSymbol];
            const price = stockInfo.data;
            const changePoint = stockInfo.change_point;
            const stock_date = stockInfo.stock_date;
            const open = price + changePoint;
            const high = open >= price ? open : price;
            const low = open >= price ? price : open;
            initial_data[stockSymbol].addData([
                {"date": stock_date, "open": open, "high": high, "low": low, "close": price}
            ]);
        });
    };
}

function ChangeChart(chart_type) {
      chart1.plot(0).dispose();
      chart2.plot(0).dispose();
      chart3.plot(0).dispose();
      chart4.plot(0).dispose();
      var chart_var1 = chart1.plot(0);
      var chart_var2 = chart2.plot(0);
      var chart_var3 = chart3.plot(0);
      var chart_var4 = chart4.plot(0);
      switch (chart_type) {
        case 'ohlc':
          chart_var1.ohlc(ohlcMapping1).name('Price');
          chart_var2.ohlc(ohlcMapping2).name('Price');
          chart_var3.ohlc(ohlcMapping3).name('Price');
          chart_var4.ohlc(ohlcMapping4).name('Price');
          break;
        case 'column':
          chart_var1.column(columnMapping1).name('High');
          chart_var2.column(columnMapping2).name('High');
          chart_var3.column(columnMapping3).name('High');
          chart_var4.column(columnMapping4).name('High');
          break;
        case 'line':
          chart_var1.area(TrendMapping1).name('Trend');
          chart_var2.area(TrendMapping2).name('Trend');
          chart_var3.area(TrendMapping3).name('Trend');
          chart_var4.area(TrendMapping4).name('Trend');
          break;
      }}


