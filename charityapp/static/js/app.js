document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event  --<< done(sort of)
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;
      const $btn = e.target.parentElement.parentElement.parentElement.dataset.id;
      const page_url = `/?page=${page}`;

      if ($btn === "1") {
        fetch(page_url)
              .then(response => response.text())
              .then(text => {
                const parser = new DOMParser();
                const htmlDocument = parser.parseFromString(text, "text/html");
                const section = htmlDocument.documentElement.querySelector("div.help--slides:nth-child(3)").innerHTML;
                e.target.parentElement.parentElement.parentElement.innerHTML = section
              });
      } else if ($btn === "2") {
         fetch(page_url)
              .then(response => response.text())
              .then(text => {
                const parser = new DOMParser();
                const htmlDocument = parser.parseFromString(text, "text/html");
                const section = htmlDocument.documentElement.querySelector("div.help--slides:nth-child(4)").innerHTML;
                e.target.parentElement.parentElement.parentElement.innerHTML = section
              });
      } else if ($btn === "3") {
        fetch(page_url)
              .then(response => response.text())
              .then(text => {
                const parser = new DOMParser();
                const htmlDocument = parser.parseFromString(text, "text/html");
                const section = htmlDocument.documentElement.querySelector("div.help--slides:nth-child(5)").innerHTML;
                e.target.parentElement.parentElement.parentElement.innerHTML = section
              });
      }
    }
  }
  // end of class help

  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation --<< done

      var $organizationId = document.querySelectorAll("div[data-step='3'] > [data-institution]");
      var selected_categories_name = [];
      var selected_categories_id = [];

      // Create an array of selected categories
      [...document.forms['form'].category].forEach(function (el) {
        if (el.checked) {
          selected_categories_id.push(parseInt(el.value));
          selected_categories_name.push(el.dataset.category_name)
        }
      });

      // Changing visibility of organizations, depends from selected categories
      for (let organization of $organizationId) {
          var org_categories = organization.dataset.categories_id.trim().split(' ').map(el => parseInt(el));
          var match_categories = [];
          selected_categories_id.forEach(function (category) {
            if (org_categories.includes(category)) {
              match_categories.push(category);
            }
            if (match_categories.length >= selected_categories_id.length) {
              organization.classList.remove("hidden-true")
            } else {
              organization.classList.add("hidden-true")
            }
          })
      }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary --<< done

      var $formSelector = document.querySelector(".form--steps-container form");
      var $summarySelector = $formSelector.querySelector("div [data-step='5']");

      // Adding number of bags to summary
      var $summaryBags = $summarySelector.querySelector("div div ul li:nth-child(1)").children[1];
      var $countBags = $formSelector.querySelector("input[name='bags']");
      // var $categoriesList = $formSelector;
      // console.log($categoriesList);
      var $summaryBagsText = "";
      if ($countBags.value === "1") {
        $summaryBagsText = `${$countBags.value} worek zawierający: ${selected_categories_name.join(", ")}`;
      }
      else if (parseInt($countBags.value) > 1 && parseInt($countBags.value) <=4) {
        $summaryBagsText = `${$countBags.value} worki zawierające: ${selected_categories_name.join(", ")}`;
      }
      else if (parseInt($countBags.value) > 4) {
        $summaryBagsText = `${$countBags.value} worków zawierających: ${selected_categories_name.join(", ")}`;
      }
       $summaryBags.innerHTML = $summaryBagsText;

      // Adding name of institution to summary
      var $allInstitution = $formSelector.querySelectorAll("input[name='organization']");
      var $summaryInstitution = $summarySelector.querySelector("div div ul li:nth-child(2)").children[1];
      var $checkedInstitution = $allInstitution[0];
      $allInstitution.forEach(function (value) {
          if (value.checked) {$checkedInstitution = value}
      });
      var $institutionText = $checkedInstitution.parentElement.querySelector("div.title").innerHTML;
      $summaryInstitution.innerHTML = `Dla: ${$institutionText} z miasta ${$formSelector.city.value}`;

      // Adding pick-up address and date, time, more info
      var $summaryAddress = $summarySelector.querySelector("div.summary div:nth-child(2) ul");
      var $summaryTermin = $summarySelector.querySelector("div.summary div:nth-child(2) div:nth-child(2) ul");

      $summaryAddress.children[0].innerHTML = $formSelector.address.value;
      $summaryAddress.children[1].innerHTML = $formSelector.city.value;
      $summaryAddress.children[2].innerHTML = $formSelector.postcode.value;
      $summaryAddress.children[3].innerHTML = $formSelector.phone.value;
      $summaryTermin.children[0].innerHTML = $formSelector.data.value;
      $summaryTermin.children[1].innerHTML = $formSelector.time.value;
      $summaryTermin.children[2].innerHTML = $formSelector.more_info.value;

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server --<< done
     */
    submit(e) {
      var $formValues = this.$form.children[1].children[1];

      function emptyValidation(value) {
        if (value === "") {
          return false
        }
        else {return true}
      }

      function validate() {
        if (
        emptyValidation($formValues.address.value) &&
        emptyValidation($formValues.city.value) &&
        emptyValidation($formValues.postcode.value) &&
        emptyValidation($formValues.phone.value) &&
        emptyValidation($formValues.data.value) &&
        emptyValidation($formValues.time.value)
      ) {
          return true
        } else {
          alert("Wszystkie pola muszą być wypełnione");
          return false
        }
      }

      if (this.currentStep === 5) {
        if (validate()) {
          this.updateForm();
        } else {
          e.preventDefault();
        }
      } else {
        e.preventDefault();
      }
      }
    }

  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
