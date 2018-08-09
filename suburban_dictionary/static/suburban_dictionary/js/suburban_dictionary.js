document.addEventListener("DOMContentLoaded", () => {
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

  if (document.querySelector(".like-dislike-container")) {
    // iterate through all like/dislike containers to add class to indicate
    // if a user has liked or disliked a term
    document.querySelectorAll(".like-dislike-container").forEach(element => {
      // get id of definition
      const definition_id = element.dataset.definition_id;

      // ajax request to get weather user has liked/disliked a definition
      const request = new XMLHttpRequest();

      request.open("POST", "/user_vote");
      request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

      request.onload = () => {
        const data = JSON.parse(request.responseText);
        const liked = data["liked"];
        const disliked = data["disliked"];

        // if user has liked the definition, add the appropriate class
        if (liked) {
          const like_button = document.querySelector(
            `#like-button-${definition_id}`
          );

          vote_button_active(like_button, definition_id);
        }

        // if user has disliked the definition, add the appropriate class
        if (disliked) {
          const dislike_button = document.querySelector(
            `#dislike-button-${definition_id}`
          );

          vote_button_active(dislike_button, definition_id);
        }
      };

      const data = JSON.stringify({
        definition_id: definition_id
      });

      request.send(data);
    });

    document.querySelectorAll(".like-button").forEach(element => {
      // on click, add like to db; if already liked by user, remove like instead
      element.addEventListener("click", () => {
        // get id of definition
        const definition_id = element.dataset.definition_id;

        // ajax request to like or remove like
        const request = new XMLHttpRequest();

        request.open("POST", "/like_definition");
        request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

        request.onload = () => {
          const data = JSON.parse(request.responseText);
          const liked = data["liked"];
          const likes_count = data["likes_count"];
          const dislikes_count = data["dislikes_count"];

          // capture like counter and button elements
          const like_counter = document.querySelector(
            `#like-counter-${definition_id}`
          );
          const like_button = document.querySelector(
            `#like-button-${definition_id}`
          );

          // update counter number with current number of likes
          like_counter.innerHTML = likes_count;

          // add or remove the class according to weather the user had liked the
          // variable
          if (liked) {
            vote_button_active(like_button, definition_id);
          } else {
            vote_button_inactive(like_button, definition_id);
          }

          // capture dislike counter and button
          const dislike_counter = document.querySelector(
            `#dislike-counter-${definition_id}`
          );
          const dislike_button = document.querySelector(
            `#dislike-button-${definition_id}`
          );

          //  if button has danger button class, remove it; update dislike number
          if (dislike_button.classList.contains("btn-danger")) {
            vote_button_inactive(dislike_button, definition_id);

            dislike_counter.innerHTML = dislikes_count;
          }
        };

        const data = JSON.stringify({
          definition_id: definition_id
        });

        request.send(data);
      });

      // when user has mouse over the button, re-color the like arrow
      element.addEventListener("mouseenter", () => {
        if (element.classList.contains("btn-outline-primary")) {
          // get id of definition
          const definition_id = element.dataset.definition_id;

          // get like arrow element
          const like_icon = document.querySelector(
            `#like-icon-${definition_id} path`
          );

          // recolor the arrow
          like_icon.style.fill = "#fcfced";
        }
      });

      // when user moves mouse out from button, re-color the like arrow
      element.addEventListener("mouseleave", () => {
        if (element.classList.contains("btn-outline-primary")) {
          // get id of definition
          const definition_id = element.dataset.definition_id;

          // get like arrow element
          const like_icon = document.querySelector(
            `#like-icon-${definition_id} path`
          );

          // recolor the arrow
          like_icon.style.fill = "#6956e2";
        }
      });
    });

    // on click, add dislike to db; if already disliked by user, remove dislike
    // instead
    document.querySelectorAll(".dislike-button").forEach(element => {
      element.addEventListener("click", () => {
        // get id of definition
        const definition_id = element.dataset.definition_id;

        if (definition_id == undefined) {
          return false;
        }

        // ajax request to like or remove like
        const request = new XMLHttpRequest();

        request.open("POST", "/dislike_definition");
        request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

        request.onload = () => {
          const data = JSON.parse(request.responseText);
          const disliked = data["disliked"];
          const dislikes_count = data["dislikes_count"];
          const likes_count = data["likes_count"];

          // capture like counter and button elements
          const dislike_counter = document.querySelector(
            `#dislike-counter-${definition_id}`
          );
          const dislike_button = document.querySelector(
            `#dislike-button-${definition_id}`
          );

          // update counter number with current number of likes
          dislike_counter.innerHTML = dislikes_count;

          // add or remove the class according to weather the user had liked the
          // variable
          if (disliked) {
            vote_button_active(dislike_button, definition_id);
          } else {
            vote_button_inactive(dislike_button, definition_id);
          }

          // capture like counter and button
          const like_counter = document.querySelector(
            `#like-counter-${definition_id}`
          );
          const like_button = document.querySelector(
            `#like-button-${definition_id}`
          );

          // if button has primary button class, remove it; update like number
          if (like_button.classList.contains("btn-primary")) {
            vote_button_inactive(like_button, definition_id);

            like_counter.innerHTML = likes_count;
          }
        };

        const data = JSON.stringify({
          definition_id: definition_id
        });

        request.send(data);
      });

      // when user has mouse over the button, re-color the like arrow
      element.addEventListener("mouseenter", () => {
        if (element.classList.contains("btn-outline-danger")) {
          // get id of definition
          const definition_id = element.dataset.definition_id;

          // get like arrow element
          const dislike_icon = document.querySelector(
            `#dislike-icon-${definition_id} path`
          );

          // recolor the arrow
          dislike_icon.style.fill = "#fcfced";
        }
      });

      // when user moves mouse out from button, re-color the like arrow
      element.addEventListener("mouseleave", () => {
        if (element.classList.contains("btn-outline-danger")) {
          // get id of definition
          const definition_id = element.dataset.definition_id;

          // get like arrow element
          const dislike_icon = document.querySelector(
            `#dislike-icon-${definition_id} path`
          );

          // recolor the arrow
          dislike_icon.style.fill = "#f24153";
        }
      });
    });
  }

  function vote_button_active(button, definition_id) {
    if (button.classList.contains("like-button")) {
      // change class to primary button
      button.classList.remove("btn-outline-primary");
      button.classList.add("btn-primary");

      // get like arrow element
      const like_icon = document.querySelector(
        `#like-icon-${definition_id} path`
      );

      // recolor the arrow
      like_icon.style.fill = "#fcfced";
    } else {
      // change class to danger button
      button.classList.remove("btn-outline-danger");
      button.classList.add("btn-danger");

      // get like arrow element
      const dislike_icon = document.querySelector(
        `#dislike-icon-${definition_id} path`
      );

      // recolor the arrow
      dislike_icon.style.fill = "#fcfced";
    }
  }

  function vote_button_inactive(button, definition_id) {
    if (button.classList.contains("like-button")) {
      // change class to primary button
      button.classList.remove("btn-primary");
      button.classList.add("btn-outline-primary");

      // get like arrow element
      const like_icon = document.querySelector(
        `#like-icon-${definition_id} path`
      );

      // recolor the arrow
      like_icon.style.fill = "#6956e2";
    } else {
      // change class to danger button
      button.classList.remove("btn-danger");
      button.classList.add("btn-outline-danger");

      // get like arrow element
      const dislike_icon = document.querySelector(
        `#dislike-icon-${definition_id} path`
      );

      // recolor the arrow
      dislike_icon.style.fill = "#f24153";
    }
  }

  //
  // delete definition
  //

  if (document.querySelector(".edit-delete-button-container")) {
    document.querySelectorAll(".delete-button").forEach(element => {
      element.addEventListener("click", () => {
        const title = "Are you sure?";
        const content = "Do you really want to delete this definition?";
        const definition_id = element.dataset.definition_id;

        generate_popup_message(title, content, definition_id);
      });
    });
  }

  //
  // popup message
  //

  function generate_popup_message(title, content, definition_id) {
    const popup_message_container = document.querySelector(
      "#popup-message-container"
    );

    const popup_message_template = Handlebars.compile(
      document.querySelector("#popup-message-template").innerHTML
    );

    const popup_message = popup_message_template({
      title: title,
      content: content,
      definition_id: definition_id
    });

    // add popup message to container, raise z-index and opacity for
    // visibility
    popup_message_container.innerHTML += popup_message;
    popup_message_container.style.zIndex = 100000;
    popup_message_container.style.opacity = 1;

    // when cancel button clicked, fade out and remove popup message
    document.querySelector("#cancel-button").addEventListener("click", () => {
      popup_message_container.style.zIndex = -1;
      popup_message_container.style.opacity = 0;
      document.querySelector("#popup-message").remove();
    });

    // when delete button clicked, send ajax request to delete the message
    document.querySelector("#delete-button").addEventListener("click", () => {
      delete_definition(definition_id);
    });
  }

  //
  // definition deletion
  //

  function delete_definition(definition_id) {
    // send ajax request to delete definition
    const request = new XMLHttpRequest();

    request.open("POST", "/delete_definition");
    request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

    request.onload = () => {
      const data = JSON.parse(request.responseText);
      const success = data["success"];
      const url = data["url"];

      if (success) {
        window.location.href = url;
      }
    };

    const data = JSON.stringify({
      definition_id: definition_id
    });

    request.send(data);
  }
});
