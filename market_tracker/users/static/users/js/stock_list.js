$(document).ready(function() {
	    var table = $('#example').on( 'draw.dt', function () {
    $("#containerexample").attr("id", "container"); $("#loadercontainer").css("display","none");
  } ).DataTable( {
	        lengthChange: true,
	        buttons: [ 'excel', 'pdf', 'colvis' ],
            "scrollX": false,
            "paging": false,
			"responsive": true,
            "order": [[ 3, "desc" ]]
	    } );
	 
	    table.buttons().container()
	        .appendTo( '#example_wrapper .col-md-6:eq(0)' );
	} );