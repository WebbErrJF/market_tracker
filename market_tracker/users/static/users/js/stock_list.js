$(document).ready(function() {
	    var table = $('#example').on( 'draw.dt', function () {
    $("#containerexample").attr("id", "container"); $("#loadercontainer").css("display","none");
  } ).DataTable( {
	        lengthChange: false,
	        buttons: [ 'excel', 'pdf', 'colvis' ],
            "scrollX": true,
            "paging": false,
            "order": [[ 3, "desc" ]]
	    } );
	 
	    table.buttons().container()
	        .appendTo( '#example_wrapper .col-md-6:eq(0)' );
	} );