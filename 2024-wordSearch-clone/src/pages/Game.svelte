<!-- Game.svelte -->
<script>
  // @ts-nocheck

  import Nav from "../components/Nav.svelte";
  import { onMount } from "svelte";
  export let params = {};

  let gameData = {};
  let wordGrid = [];
  let ws;

  const BASE_URL = "http://localhost:8000";
  const gameId = params.gameId;
  let username = ""; // 사용자 이름을 저장할 변수

  console.log(gameId);

  async function fetchGameData() {
    try {
      const response = await fetch(`${BASE_URL}/get_game_info/${gameId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      gameData = await response.json();
      console.log(gameData);
      const grid = await generateWordGrid(10);
      console.log(grid);
    } catch (error) {
      console.error("Error fetching game data:", error);
    }
  }

  function generateRandomChar() {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return alphabet[Math.floor(Math.random() * alphabet.length)];
  }

  async function generateWordGrid(size) {
    // 게임 정보에서 단어 목록 추출
    const words = gameData.game_info.words.map((wordObj) => wordObj.word);

    // 그리드 초기화
    wordGrid = [];

    // 그리드 생성
    for (let i = 0; i < size; i++) {
      let row = [];
      for (let j = 0; j < size; j++) {
        // 무작위 알파벳 선택
        const randomChar = generateRandomChar();
        row.push(randomChar);
      }
      wordGrid.push(row);
    }
    return wordGrid;
  }

  onMount(() => {
    fetchGameData();

    ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connection established.");
      // 사용자 이름을 서버에 전송
      ws.send(JSON.stringify({ type: "username", data: username }));
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onmessage = (event) => {
      console.log("Message from server:", event.data);
      // 서버로부터 메시지를 받아서 처리하는 로직을 추가할 수 있습니다.
    };
  });

  function startGame() {
    // 사용자 이름을 얻어옴
    const input = document.getElementById("username");
    if (input && input.value.trim() !== "") {
      username = input.value.trim();
      // 게임을 시작하기 전에 사용자 이름을 서버에 전송
      ws.send(JSON.stringify({ type: "start", data: { username, gameId } }));
    } else {
      alert("사용자 이름을 입력하세요.");
    }
  }
</script>

<Nav location="game"></Nav>

<main class="game-container-custom">
  <!-- 게임 시작 폼 -->
  <form on:submit|preventDefault={startGame}>
    <label for="username">사용자 이름:</label>
    <input type="text" id="username" name="username" required />
    <button type="submit">시작</button>
  </form>

  <!-- 게임 UI -->
  <div class="word-search-custom">
    <!-- Word search game area -->
    <table>
      <!-- Loop through wordGrid to display the grid -->
      {#each wordGrid as row}
        <tr>
          {#each row as letter}
            <td>{letter}</td>
          {/each}
        </tr>
      {/each}
    </table>
  </div>

  <!-- Sidebar -->
  <div class="sidebar-custom">
    <!-- Word list -->
    <div class="word-list-custom">
      <h3>단어 목록</h3>
      <ul>
        <!-- Display word list if it's not empty and iterable -->
        {#if gameData.words && gameData.words.length > 0}
          {#each gameData.words as word}
            <li>{word}</li>
          {/each}
        {:else}
          <li>단어 없음</li>
        {/if}
      </ul>
    </div>

    <!-- Status board -->
    <div class="status-board-custom">
      <h3>상태 보드</h3>
      <ul>
        <!-- Display user scores and time -->
        <li class="user-score">유저 1: 100 점</li>
        <li class="user-score">유저 2: 80 점</li>
        <li class="user-score">유저 3: 60 점</li>
      </ul>
    </div>
  </div>

  <!-- Timer -->
  <div class="timer-custom">
    <h3>타이머</h3>
    <span id="timer">00:00</span>
  </div>
</main>

<style>
  /* Game styles */
  .game-container-custom {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px;
  }

  .word-search-custom {
    flex: 1;
    margin-right: 20px;
    /* Add styles for the word search game area */
  }

  .word-search-custom table {
    border-collapse: collapse;
  }

  /* .word-search-custom td {
  width: 30px;
  height: 30px;
  border: 1px solid #ccc;
  text-align: center;
  vertical-align: middle;
} */

  .sidebar-custom {
    flex: 0 0 300px;
    /* Add styles for the sidebar */
  }

  .word-list-custom {
    /* Add styles for the word list */
    font-size: 16px;
    padding-left: 10px;
  }

  .word-list-custom ul {
    padding: 0;
    list-style-type: none;
  }

  .status-board-custom {
    /* Add styles for the status board */
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
  }

  .status-board-custom ul {
    padding: 0;
    list-style-type: none;
    margin: 0;
  }

  .user-score {
    margin-bottom: 5px;
  }

  .timer-custom {
    /* Add styles for the timer */
    color: #ff0000;
    font-size: 20px;
    font-weight: bold;
  }
</style>
