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
let sequence1 = document.querySelector("#sequence1");
sequence1.addEventListener("click", e => {
  console.log("click");
  // window.location.href = "/level?key="+sequence1_key.content;
  window.location.href = "/level?sequence=1&key="+sequence1_key.content;
});

////For sequences 2 and three
// let sequence2 = document.querySelector("#sequence2");
// sequence1.addEventListener("click", e => {
//   console.log("click");
//    window.location.href = "/level?sequence=2&key="+sequence2_key.content;
// });
// let sequence3 = document.querySelector("#sequence3");
// sequence1.addEventListener("click", e => {
//   console.log("click");
//     window.location.href = "/level?sequence=3&key="+sequence3_key.content;
// });
