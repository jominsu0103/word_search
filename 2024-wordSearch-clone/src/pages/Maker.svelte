<script>
  // @ts-nocheck

  import Nav from "../components/Nav.svelte";

  let title = "";
  let description = "";
  let words = Array.from({ length: 30 }).fill("");
  let gameUrl = "";

  const BASE_URL = "http://localhost:8000";

  async function submitGameInfo() {
    const filteredWords = words
    .map(word => word.trim().toUpperCase())
    .filter(word => word !== "");

    // 최소 10개의 단어가 있는지 확인
    if (filteredWords.length < 10) {
      console.error("최소 10개의 단어를 입력해야 합니다.");
      return;
    }

    console.log(
      `title: ${title} description: ${description} words: ${filteredWords}`
    );

    const accessToken = localStorage.getItem("accessToken");
    console.log(accessToken);

    const data = { title, description, words: filteredWords, accessToken };

    try {
      const response = await fetch(`${BASE_URL}/save_game_info`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      const responseData = await response.json();
      gameUrl = responseData.game_url;
      console.log(gameUrl);
      await updateGameInfo(gameUrl);
    } catch (error) {
      console.error("오류 발생:", error);
    }
  }

  async function updateGameInfo(gameUrl) {
  const gameId = gameUrl.split("/").pop();
  const data = {
    url: gameUrl,
    gameId: gameId
  }
  try {
    const response = await fetch(`${BASE_URL}/update_game_info_for_url`,{
      method: "PUT",
      headers:{
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    })
    const responseData = await response.json();
    console.log(responseData)
  } catch (error) {
    console.error("오류 발생:",error);
  }
}
</script>

<Nav location="maker"></Nav>
<main>
  <div class="manage-container">
    <button class="manage-btn"> Manage existing puzzles here </button>
  </div>
  <div class="title-container">
    <div>Title</div>
    <div class="title-input">
      <input bind:value={title} type="text" required />
    </div>
  </div>
  <div class="desc-container">
    <div>Description</div>
    <div class="desc-input">
      <input bind:value={description} type="text" required />
    </div>
  </div>
  <div class="word_list-container">
    <div>Word List</div>
    <div>
      Between 10 and 30 words. Puzzles are randomly generated using a selection
      of your words at play time.
    </div>
    <div class="table-container">
      {#each Array.from({ length: 6 }) as _, rowIndex}
        <div class="table-row" key={rowIndex}>
          {#each Array.from({ length: 5 }) as _, cellIndex}
            {#if rowIndex * 5 + cellIndex < 30}
              <div class="table-cell" key={cellIndex}>
                <input
                  type="text"
                  bind:value={words[rowIndex * 5 + cellIndex]}
                />
              </div>
            {/if}
          {/each}
        </div>
      {/each}
    </div>
  </div>
  <!-- <div class="table-container">
      <div class="table-row">
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
      </div>
      <div class="table-row">
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
      </div>
      <div class="table-row">
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
      </div>
      <div class="table-row">
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
      </div>
      <div class="table-row">
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
        <div class="table-cell"><input type="text" /></div>
      </div>
    </div> -->
  <div class="btnOrange-container">
    <button on:click={submitGameInfo} class="btnPush btnOrange">Submit</button>
  </div>
  {#if gameUrl}
    <div>
      <span>게임 URL:</span>
      <span>{gameUrl}</span>
    </div>
  {/if}
</main>
<footer>
  <div class="instructions">
    <div>Instructions</div>
    <ul>
      <li>
        To create a word search puzzle you must supply a word list of at least
        10 words.
      </li>
      <li>
        The word list should be based on a single theme or topic. For example a
        television show or a movie you enjoy.
      </li>
      <li>
        Words can only contain the letters a-z and a maximum of two spaces or
        dashes.
      </li>
      <li>
        Spaces and dashes will be removed when words are added to the word
        search grid.
      </li>
      <li>Words can have a maximum length of 14 letters</li>
      <li>
        Do not include any personally identifiable information in your puzzles
      </li>
    </ul>
  </div>
</footer>
