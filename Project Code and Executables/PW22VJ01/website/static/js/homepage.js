const navAnimation = function () {
    const burger = document.querySelector(".burger"); 
    const navtrans = document.querySelector(".nav-links"); 
    const navLinks = document.querySelectorAll(".nav-links li");

    burger.addEventListener('click', () => {
        navtrans.classList.toggle('nav-active');

       navLinks.forEach((link,index)=>{
           if(link.style.animation){
               link.style.animation = '';
           }else {
            link.style.animation = `navLinkFade 0.5 ease forwards ${index+1.2}s`
           }
       });
       burger.classList.toggle('animateBurger')

    }); 
}

navAnimation();  

