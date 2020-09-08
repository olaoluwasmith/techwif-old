myButton = document.getElementById('myBtn');
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 ||
        document.elementFromPoint.scrollTop > 20) {
            mybutton.style.display = 'block';
        } else {
            mybutton.style.display = 'none';
        };
};

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
};

$(document).ready(function(e){
    $('.reply-btn').click(function() {
        $(this).parent().parent().next('.replied-comments').fadeToggle();
    });
});


var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action);

        console.log('USER:', user);
        if(user == 'AnonymousUser'){
            addCookieItem(productId, action);
        }else{
            updateUserOrder(productId, action);
        }
    })
}


function addCookieItem(productId, action){
    console.log('Not logged in...');
    
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item');
            delete cart[productId]
        }
    }
    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()  
}


function updateUserOrder(productId, action){
    console.log("User is logged in, sending data...");

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data);
        location.reload()
    })
}


let thumbnails = document.getElementsByClassName('thumbnail-product')

let activeImages = document.getElementsByClassName('active')

for (var i=0; i < thumbnails.length; i++){
    thumbnails[i].addEventListener('mouseover', function(){
        console.log(activeImages)

        if (activeImages.length > 0){
            activeImages[0].classList.remove('active')
        }

        this.classList.add('active')
        document.getElementById('featured').src = this.src
    })
}

let buttonRight = document.getElementById('slideRight');
let buttonLeft = document.getElementById('slideLeft');

buttonLeft.addEventListener('click', function(){
    document.getElementById('slider').scrollLeft -= 180
})

buttonRight.addEventListener('click', function(){
    document.getElementById('slider').scrollLeft += 180
})
