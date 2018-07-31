let box = document.querySelector("#sequence1");

  console.log(box);
  box.addEventListener("mouseenter", e=> {
    console.log('mousenter', e);
    box.classList.add("spin");
  });

  box.addEventListener("mouseleave", e=> {
    box.classList.remove("spin");
  });
