document.addEventListener("DOMContentLoaded", () => {
  fitty(".hero-title");
  fitty(".hero-subtitle");

  //
  // fetch scrf token
  //

  // http://musings.tinbrain.net/blog/2015/aug/28/vanilla-js-meets-djangos-csrf/
  function parse_cookies() {
    var cookies = {};
    if (document.cookie && document.cookie !== "") {
      document.cookie.split(";").forEach(function(c) {
        var m = c.trim().match(/(\w+)=(.*)/);
        if (m !== undefined) {
          cookies[m[1]] = decodeURIComponent(m[2]);
        }
      });
    }
    return cookies;
  }

  var cookies = parse_cookies();

  //
  // like/dislike definition
  //

  // on click, add like to db; if already liked by user, remove like instead
  if (document.querySelector(".like-dislike-container")) {
    document.querySelectorAll(".like-button").forEach(element => {
      element.addEventListener("click", () => {
        // get id of definition
        const definition_id = element.dataset.definition_id;

        if (definition_id == undefined) {
          return false;
        }

        // ajax request to like or remove like
        const request = new XMLHttpRequest();

        request.open("POST", "/like_definition");
        request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

        request.onload = () => {};

        const data = JSON.stringify({
          definition_id: definition_id
        });

        request.send(data);
      });
    });
  }
});
