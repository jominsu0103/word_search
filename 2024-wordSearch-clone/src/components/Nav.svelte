<script>
  export let location;
  const moveToMaker = () => {
    window.location.hash = "/maker";
  };

  const moveToMyPage = () => {
    window.location.hash = "/mypage";
  };

  const moveToHome = () => {
    window.location.hash = "/";
  };
</script>

<header>
  <div class="header-container">
    <div class="header-title">Word Search</div>
    <div class="header-icons">
      <button class="header-icons_btn" on:click={moveToMaker}>
        <img src="assets/maker.svg" alt="maker" />
        <div class="description maker">Maker</div>
      </button>
      <button class="header-icons_btn" on:click={moveToHome}>
        <img src="assets/home.svg" alt="home" />
        <div class="description home">Home</div>
      </button>
      <button class="header-icons_btn" on:click={moveToMyPage}>
        <img src="assets/mypage.svg" alt="mypage" />
        <div class="description mypage">Mypage</div>
      </button>
    </div>
  </div>
</header>
<hr />
