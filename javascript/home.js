let box = document.querySelector(".sequence");

  console.log(box);
  box.addEventListener("mouseenter", e=> {
    console.log('mousenter', e);
    box.classList.add("shade");
  });

  box.addEventListener("mouseleave", e=> {
    box.classList.remove("shade");
  });
