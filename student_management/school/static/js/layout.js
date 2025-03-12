const headerItemList = document.querySelector(".header-item-list");
const headerAvatar = document.querySelector(".header-avatar");

const handleShowAvatarMenu = () => {
  headerItemList.classList.toggle("active");
};

// Ẩn menu khi click ra ngoài
document.addEventListener("click", (event) => {
  if (
    !headerItemList.contains(event.target) &&
    !headerAvatar.contains(event.target)
  ) {
    headerItemList.classList.remove("active");
  }
});
