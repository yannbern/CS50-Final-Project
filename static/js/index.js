"use strict";

// Query selectors
const logInBtn = document.querySelector(".btn--login");
const signUpBtn = document.querySelector(".btn--signup");
const addBtn = document.querySelector(".btn--add");
const modal = document.querySelector(".modal");
const modalError = document.querySelector(".modal-error");
const modalCloseBtn = document.querySelectorAll(".modal-close-icon");
const signUpForm = document.querySelector(".sign-up-form");
const signInForm = document.querySelector(".sign-in-form");
const listingForm = document.querySelector(".listing-form");
const listingContainer = document.querySelector(".listing-container");
const listingImage = document.querySelectorAll(".listing-img-container");
const viewModal = document.querySelector(".view-modal");
const viewImg = document.querySelector(".view-img");
const viewTitle = document.querySelector(".view-title");
const viewPrice = document.querySelector(".view-price");
const viewDescription = document.querySelector(".view-description");
const viewCondition = document.querySelector(".view-condition");
const viewButton = document.querySelector(".btn--view");
const emailFields = document.querySelectorAll("#email-signup, #email-signin");
const passwordField = document.querySelector("#password-signup");
const nameField = document.getElementById("name");
const forgotBtn = document.querySelectorAll(".forgot");

// Format currency function
const formatCurrency = (number) => {
  if (Number.isInteger(number)) {
    return number.toLocaleString();
  } else {
    const formatted = number.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    return formatted.replace(/(\.00|\.0)$/, "");
  }
};

// Close modal when close button clicked
modalCloseBtn.forEach((btn) => {
  btn.addEventListener("click", () => {
    modal.classList.toggle("hidden");
    signInForm.classList.add("hidden");
    signUpForm.classList.add("hidden");
    listingForm.classList.add("hidden");
    viewModal.classList.add("hidden");
  });
});

// Open listing form
addBtn.addEventListener("click", () => {
  modal.classList.toggle("hidden");
  listingForm.classList.toggle("hidden");
});

// Switch between signin / signup forms
forgotBtn.forEach((btn) => {
  btn.addEventListener("click", () => {
    signInForm.classList.toggle("hidden");
    signUpForm.classList.toggle("hidden");
  });
});

// Sign up/in buttons (Event delegation)
document.body.addEventListener("click", (e) => {
  if (e.target === signUpBtn) {
    modal.classList.toggle("hidden");
    signUpForm.classList.toggle("hidden");
  } else if (e.target === logInBtn) {
    e.preventDefault();
    modal.classList.toggle("hidden");
    signInForm.classList.toggle("hidden");
  }
});

// Show listing details
listingImage.forEach((image) => {
  image.addEventListener("click", function (e) {
    if (e.target.classList.contains("overlay-icon--right")) {
      return;
    }
    modal.classList.toggle("hidden");
    viewModal.classList.remove("hidden");

    const listingId = image.closest(".listing").dataset.listingId;

    fetch(`/listing/${listingId}`)
      .then((response) => response.json())
      .then((data) => {
        viewImg.src = `/static/uploads/${data.ImageFilePath}`;
        viewTitle.textContent = `${data.Title}`;
        viewPrice.textContent = `£${formatCurrency(data.Price)}`;
        viewCondition.textContent = data.Condition;
        viewDescription.textContent = `${data.Description}`;
        fetch(`/user/${data.UserID}`)
          .then((response2) => response2.json())
          .then((data2) => {
            viewButton.href = `mailto:${data2[2]}`;
            console.log(viewButton);
          });
      });
  });
});

// Delete listing
document.body.addEventListener("click", (e) => {
  if (e.target.classList.contains("overlay-icon--right")) {
    const listing = e.target.parentNode.parentNode.parentNode;
    const listingId = listing.dataset.listingId;
    fetch(`/delete-listing/${listingId}`, { method: "DELETE" }).then(
      (response) => {
        if (response.ok) {
          window.location.reload();
        }
      }
    );
  }
});

// Category carousel
const scrollForward = document.querySelector(".main-nav-icon--scroll");
const scrollBack = document.querySelector(".main-nav-icon--scroll.back");
const carousel = document.querySelector(".main-nav-scroll");
if (
  window.location.pathname === "/category/homegarden" ||
  window.location.pathname === "/category/booksmedia" ||
  window.location.pathname === "/category/other"
) {
  carousel.scrollLeft += 400;
} else if (window.location.pathname === "/category/clothes") {
  carousel.scrollLeft += 200;
}
scrollForward.addEventListener("click", () => {
  carousel.scrollLeft += 200;
  manageScrollPosition();
});
scrollBack.addEventListener("click", () => {
  carousel.scrollLeft -= 200;
  manageScrollPosition();
});
carousel.addEventListener("scroll", manageScrollPosition);

function manageScrollPosition() {
  if (carousel.scrollLeft >= 20) {
    scrollBack.classList.remove("hidden");
  } else {
    scrollBack.classList.add("hidden");
  }

  let maxScrollValue = carousel.scrollWidth - carousel.clientWidth - 20;
  if (carousel.scrollLeft >= maxScrollValue) {
    scrollForward.classList.add("hidden");
  } else {
    scrollForward.classList.remove("hidden");
  }
}

// Image preview function
function handleFileUpload(event) {
  const fileInput = event.target;
  const file = fileInput.files[0];
  const reader = new FileReader();

  const allowedExtensions = ["jpg", "jpeg", "png"];
  const fileExtension = file.name.split(".").pop().toLowerCase();
  if (!allowedExtensions.includes(fileExtension)) {
    alert("Only JPEG, JPG, and PNG files are allowed.");
    return;
  }

  reader.onload = function (e) {
    const previewDiv = document.querySelector(".custom-file-input");
    previewDiv.style.backgroundImage = `url(${e.target.result})`;
    document.querySelector(".photo-input-logo").classList.add("hidden");
    document.querySelector(".photo-input-text").classList.add("hidden");
    document.querySelector(".photo-input-remove").classList.remove("hidden");
  };
  reader.readAsDataURL(file);
}

document
  .querySelector(".photo-input-remove")
  .addEventListener("click", (el) => {
    document.querySelector(".custom-file-input").style.backgroundImage = "none";
    document.querySelector(".photo-input-logo").classList.remove("hidden");
    document.querySelector(".photo-input-text").classList.remove("hidden");
    document.querySelector(".photo-input-remove").classList.add("hidden");
    document.querySelector(".photo-input").value = "";
  });
const fileInput = document.querySelector(".photo-input");
fileInput.addEventListener("change", handleFileUpload);

// Regex expression
emailFields.forEach((field) => {
  field.addEventListener("input", () => {
    const errorModal = field.nextElementSibling;
    errorModal.classList.add("hidden");
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const inputValue = field.value;
    if (!regex.test(inputValue)) {
      field.classList.add("modal-incorrect");
    } else {
      field.classList.remove("modal-incorrect");
    }
  });
  field.addEventListener("invalid", (e) => {
    e.preventDefault();
    const errorModal = field.nextElementSibling;
    errorModal.classList.remove("hidden");
  });
});
passwordField.addEventListener("input", (e) => {
  const errorModal = passwordField.nextElementSibling;
  errorModal.classList.add("hidden");
  const regex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  const inputValue = passwordField.value;
  if (!regex.test(inputValue) && inputValue > 0) {
    passwordField.classList.add("modal-incorrect");
  } else {
    passwordField.classList.remove("modal-incorrect");
  }
});
passwordField.addEventListener("invalid", (e) => {
  e.preventDefault();
  const errorModal = passwordField.nextElementSibling;
  errorModal.classList.remove("hidden");
});
nameField.addEventListener("input", () => {
  const regex = /^[a-zA-Z0-9]{2,20}$/;
  const inputValue = nameField.value;
  if (!regex.test(inputValue) && inputValue.length > 2) {
    nameField.classList.add("modal-incorrect");
  } else {
    nameField.classList.remove("modal-incorrect");
  }
});

// Flash message
const flashMessage = document.querySelector(".flash");
if (flashMessage) {
  flashMessage.offsetWidth;
  flashMessage.classList.add("slide-up");
  setTimeout(() => {
    flashMessage.classList.add("slide-down");
  }, 2000);
  setTimeout(() => {
    flashMessage.classList.add("hidden");
  }, 2500);
}

// Mobile carousel
const mobileCarousel = document.querySelector(".mobile-nav-list");
let dragging = false;
const drag = (e) => {
  if (!dragging) return;
  mobileCarousel.scrollLeft -= e.movementX;
};
mobileCarousel.addEventListener("mousedown", () => {
  dragging = true;
});
mobileCarousel.addEventListener("mousemove", drag);
document.addEventListener("mouseup", () => {
  dragging = false;
});
