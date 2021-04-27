/* Fixed navbar after scroll */

document.addEventListener("DOMContentLoaded", function(){
  window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        document.getElementById('mainNav').classList.add('navbar_scroll');
        // document.getElementById('mainNav').classList.remove("navbar-dark");
        // add padding top to show content behind navbar
        // navbar_height = document.querySelector('.navbar').offsetHeight;
        // document.body.style.paddingTop = navbar_height + 'px';
      }
      else {
        document.getElementById('mainNav').classList.remove('navbar_scroll');
         // remove padding top from body
        document.body.style.paddingTop = '0';
      }
  });
});

// $(document).ready(function () {
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 // Does this cookie string begin with the name we want?
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
//
//     const csrftoken = getCookie('csrftoken');
//
//     $("button").click(function (e) {
//         // var product_id = $('#productId')
//         // console.log(e.target.nodeName)
//         var data = $.parseJSON($(this).attr('data-button'));
//         var id = $(this).attr('id');
//         console.log(data)
//         console.log(id)
//         // console.log(product_id.val())
//         e.preventDefault();
//
//
//         $.ajax({
//             type: "POST",
//             url: "/products/" + data + "/save/",
//             // dataType: 'json',
//             data: {
//                 data: data,
//                 csrfmiddlewaretoken: csrftoken,
//             },
//
//             success: function (data) {
//                 if (data.result === false) {
//                     alert("une erreur s'est produite lors de la sauvegarde de votre produit. Veuillez réessayer !!")
//                 } else {
//                     alert("Produit ajouté")
//                     $('#' + id).css("background-color", "green")
//                 }
//
//             }
//         });
//
//
//     });
// });
// $("button").click(function (e) {
//         // var product_id = $('#productId')
//         // console.log(e.target.nodeName)
//         var data = $.parseJSON($(this).attr('data-button'));
//         console.log(data)
//         // console.log(product_id.val())
//         e.preventDefault();
//
//
//         $.ajax({
//             type: "POST",
//             url: "/products/" + data +"/save/",
//             dataType: 'json',
//             data: data,
//             success: function (data){
//                 console.log(data)
//             }
//         });
//
//
//     });