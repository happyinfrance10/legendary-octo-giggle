// Darken each sequence box when mouse goes over it
let sequences = document.querySelectorAll("span");
  sequences.forEach(sequence => {

  console.log(sequence);
  sequence.addEventListener("mouseenter", e=> {
    console.log('mousenter', e);
    sequence.classList.add("shade");
  });

  sequence.addEventListener("mouseleave", e=> {
    sequence.classList.remove("shade");
  });
});

let sequence1_key = document.getElementById('sequence1_key');
<<<<<<< HEAD
=======
let sequence2_key = document.getElementById('sequence2_key');
let sequence3_key = document.getElementById('sequence3_key');
let sequence4_key = document.getElementById('sequence4_key');


>>>>>>> 92759943ca2e1a8a1151ec18896df7250f7f492a
let sequence1 = document.querySelector("#sequence1");
sequence1.addEventListener("click", e => {
  window.location.href = "/level?sequence=1&key="+sequence1_key.content;
});

////For sequences 2 and three
let sequence2 = document.querySelector("#sequence2");
sequence2.addEventListener("click", e => {
   window.location.href = "/level?sequence=2&key="+sequence2_key.content;
});
let sequence3 = document.querySelector("#sequence3");
sequence3.addEventListener("click", e => {
    window.location.href = "/level?sequence=3&key="+sequence3_key.content;
});
let sequence4 = document.querySelector("#sequence4");
sequence4.addEventListener("click", e => {
   window.location.href = "/level?sequence=4&key="+sequence4_key.content;
});
