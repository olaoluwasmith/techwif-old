    /*
        $(document).on('submit', '.comment-form', function(event) {
            event.preventDefault();
            console.log( $(this).serialize() );
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: 'json',

                success:function(response) {
                    $('.main-comment-section').html(response['form']);
                    $('textarea').val('');
                    $('.reply-btn').click(function() {
                        $(this).parent().parent().next('.replied-comments').fadeToggle();
                        $('textarea').val('');
                    });
                },
                error:function(rs, e) {
                    console.log(rs.responseText);
                },
            });
        });


        $(document).on('submit', '.reply-form', function(e){
            e.preventDefault();
            console.log($(this).serialize());
            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: 'json',
                success: function(response){
                    $('.main-comment-section').html(response['form']);
                    $('textarea').val('');
                    $('.reply-btn').click(function() {
                        $(this).parent().parent().next('.replied-comments').fadeToggle();
                        $('textarea').val('');
                    });
                },
                error: function(rs, e) {
                    console.log(rs.responseText);
                },
            });
        }); 


<script src="https://www.paypal.com/sdk/js?client-id=ASMpNtoKF6QkIq-em804PJjIWwk-gT-kkqd55Hvvrs7BKRRGdF1c_B1gU-zupp_2nK1TGMVRSZqbq-jy&currency=USD"></script>

<script>
    var total = '{{ order.get_cart_total }}'

    paypal.Buttons({
      createOrder: function(data, actions) {
        // This function sets up the details of the transaction, including the amount and line item details.
        return actions.order.create({
          purchase_units: [{
            amount: {
              value: parseFloat(total).toFixed(2)
            }
          }]
        });
      },
      onApprove: function(data, actions) {
        // This function captures the funds from the transaction.
        return actions.order.capture().then(function(details) {
            submitFormData()
        });
      }
    }).render('#paypal-button-container');
    //This function displays Smart Payment Buttons on your web page.
</script> */