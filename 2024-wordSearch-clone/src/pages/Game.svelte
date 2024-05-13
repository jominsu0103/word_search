<!-- Game.svelte -->
<script>
  //@ts-nocheck
  import Nav from "../components/Nav.svelte";
  import { onMount } from "svelte";
  export let params = {};

  let gameData = {};
  let wordGrid = [];
  let ws;
  let gameWord = {};
  let timerInterval;
  let timeRemaining = 300;
  let isDragging = false;
  let selectedCells = [];

  const BASE_URL = "http://localhost:8000";
  const gameId = params.gameId;
  let username = "";

  async function fetchGameData() {
    try {
      const response = await fetch(`${BASE_URL}/get_game_info/${gameId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      gameData = await response.json();
      gameWord = gameData.game_info.words;
      const grid = await generateWordGrid(10);
    } catch (error) {
      console.error("Error fetching game data:", error);
    }
  }

  function generateRandomChar() {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return alphabet[Math.floor(Math.random() * alphabet.length)];
  }

  async function generateWordGrid(size) {
    const words = gameData.game_info.words.map((wordObj) => wordObj.word);

    wordGrid = Array.from({ length: size }, () =>
      Array.from({ length: size }, () => "")
    );

    for (const word of words) {
      await placeWord(word);
    }

    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        if (wordGrid[i][j] === "") {
          wordGrid[i][j] = generateRandomChar();
        }
      }
    }
  }

  async function placeWord(word) {
    const directions = [
      [-1, 0],
      [1, 0],
      [0, -1],
      [0, 1],
      [-1, -1],
      [-1, 1],
      [1, -1],
      [1, 1],
    ];

    let startX = Math.floor(Math.random() * wordGrid.length);
    let startY = Math.floor(Math.random() * wordGrid.length);
    let direction = directions[Math.floor(Math.random() * directions.length)];

    while (
      startX + direction[0] * word.length < 0 ||
      startY + direction[1] * word.length < 0 ||
      startX + direction[0] * word.length >= wordGrid.length ||
      startY + direction[1] * word.length >= wordGrid.length
    ) {
      startX = Math.floor(Math.random() * wordGrid.length);
      startY = Math.floor(Math.random() * wordGrid.length);
      direction = directions[Math.floor(Math.random() * directions.length)];
    }

    let currentX = startX;
    let currentY = startY;
    let wordFits = true;

    for (let i = 0; i < word.length; i++) {
      if (
        wordGrid[currentX][currentY] !== "" &&
        wordGrid[currentX][currentY] !== word[i]
      ) {
        wordFits = false;
        break;
      }
      currentX += direction[0];
      currentY += direction[1];
    }

    if (wordFits) {
      currentX = startX;
      currentY = startY;
      for (let i = 0; i < word.length; i++) {
        wordGrid[currentX][currentY] = word[i];
        currentX += direction[0];
        currentY += direction[1];
      }
    } else {
      await placeWord(word);
    }
  }

  function updateTimer() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const formattedTime = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    document.getElementById("timer").innerText = formattedTime;
    timeRemaining--;
    if (timeRemaining < 0) {
      clearInterval(timerInterval);
    }
  }

  function handleMouseDown(event , rowIdx , colIdx) {
    isDragging = true;
    selectedCells = [{rowIdx , colIdx}]
    event.target.classList.add('highlight');
  }

  function handleMouseMove(event, rowIdx, colIdx) {
  if (isDragging) {
    // 현재 선택된 셀과 새로운 셀 사이의 모든 셀을 선택
    const lastSelectedCell = selectedCells[selectedCells.length - 1];
    const rowStep = Math.sign(rowIdx - lastSelectedCell.rowIdx);
    const colStep = Math.sign(colIdx - lastSelectedCell.colIdx);
    let currentRow = lastSelectedCell.rowIdx;
    let currentCol = lastSelectedCell.colIdx;

    while (currentRow !== rowIdx || currentCol !== colIdx) {
      currentRow += rowStep;
      currentCol += colStep;
      if (!selectedCells.find(cell => cell.rowIdx === currentRow && cell.colIdx === currentCol)) {
        selectedCells.push({ rowIdx: currentRow, colIdx: currentCol });
        document.querySelector(`.cell[row-index="${currentRow}"][col-index="${currentCol}"]`).classList.add('highlight');
      }
    }
  }
}

  function handleMouseUp() {
    isDragging = false;
    checkSelectedWord();
    selectedCells = [];
    document.querySelectorAll(".highlight").forEach(cell => cell.classList.remove('highlight'));
  }

  function checkSelectedWord(){
    const word = selectedCells.map(cell => wordGrid[cell.rowIdx][cell.colIdx]).join('')
    console.log(word)
    verifyWord(word)
  }

  function handleKeyDown(event , rowIdx , colIdx){
    if (event.key === 'Enter' || event.key === ' ') {
      handleCellClick(event, rowIdx, colIdx)
    }
  }

  async function verifyWord(selectedWord){
    try {
      const response = await fetch(`${BASE_URL}/verify-word`,{
        method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({gameId:gameId, word: selectedWord})
      })
      const result = await response.json();
      if (result.correct) {
        console.log('정답입니다!');
        // 추가적인 정답 처리 로직
      } else if(!result.correct) {
        console.log('틀렸습니다. 다시 시도하세요.');
        // 추가적인 오류 처리 로직
      }
    } catch (error) {
      console.error('Error verifying word:', error);
    }
  }

  onMount(() => {
    fetchGameData();

    ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connection established.");
      ws.send(JSON.stringify({ type: "username", data: username }));
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onmessage = (event) => {
      console.log("Message from server:", event.data);
    };
  });

  function handleCellClick(event, rowIdx, colIdx) {
    const clickedLetter = wordGrid[rowIdx][colIdx];
    const clickedWord = gameWord.find((wordObj) => wordObj.word.includes(clickedLetter));
    if (clickedWord) {
      event.target.classList.add('correct');
    } else {
      alert('잘못된 선택입니다. 정답을 찾으세요.');
    }
  }

  function startGame() {
    const input = document.getElementById("username");
    if (input && input.value.trim() !== "") {
      username = input.value.trim();
      timerInterval = setInterval(updateTimer, 1000);
      ws.send(JSON.stringify({ type: "start", data: { username, gameId } }));
    } else {
      alert("사용자 이름을 입력하세요.");
    }
  }
  startGame();
</script>

<Nav location="game"></Nav>

<main class="game-container-custom">
  <div class="start-form">
    <form on:submit|preventDefault={startGame}>
      <label for="username">사용자 이름:</label>
      <input type="text" id="username" name="username" required />
      <button type="submit">시작</button>
    </form>
  </div>

  <div class="word-search-custom">
    {#each wordGrid as row, rowIndex}
      {#each row as letter, colIndex}
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div
          class="cell"
          on:mousedown={(event) => handleMouseDown(event, rowIndex, colIndex)}
          on:mousemove={(event) => handleMouseMove(event, rowIndex, colIndex)}
          on:mouseup={handleMouseUp}
          on:keydown={(event) => handleKeyDown(event, rowIndex, colIndex)}
        >
          {letter}
        </div>
      {/each}
    {/each}
  </div>

  <div class="sidebar-custom">
    <div class="timer-custom">
      <h3>타이머</h3>
      <span id="timer">00:00</span>
    </div>

    <div class="word-list-custom">
      <h3>단어 목록</h3>
      <ul>
        {#if gameWord && gameWord.length > 0}
          {#each gameWord as word}
            <li>{word.word}</li>
          {/each}
        {:else}
          <li>단어 없음</li>
        {/if}
      </ul>
    </div>

    <div class="status-board-custom">
      <h3>상태 보드</h3>
      <ul>
        <li class="user-score">유저 1: 100 점</li>
        <li class="user-score">유저 2: 80 점</li>
        <li class="user-score">유저 3: 60 점</li>
      </ul>
    </div>
  </div>
</main>

<style>
.game-container-custom {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px;
  }

  .word-search-custom {
    display: grid;
    grid-template-columns: repeat(10, 40px); /* 10 columns, each 40px wide */
    grid-gap: px;
    margin-right: 20px;
  }

  .cell {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #ccc;
    user-select: none; /* Prevent text selection */
  }

  .cell:focus{
    outline: none;
    border-color: blue;
  }

  .sidebar-custom {
    flex: 0 0 300px;
  }

  .word-list-custom {
    font-size: 16px;
    padding-left: 10px;
  }

  .word-list-custom ul {
    padding: 0;
    list-style-type: none;
  }

  .status-board-custom {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    margin-top: 20px;
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
    color: #ff0000;
    font-size: 20px;
    font-weight: bold;
    margin-top: 20px;
  }

</style>
