<script>
  import Nav from "../components/Nav.svelte";
</script>

<Nav location="maker"></Nav>
<main>
  <div class="manage-container">
    <button class="manage-btn"> Manage existing puzzles here </button>
  </div>
  <div class="title-container">
    <div>Title</div>
    <div class="title-input">
      <input type="text" required />
    </div>
  </div>
  <div class="desc-container">
    <div>Description</div>
    <div class="desc-input">
      <input type="text" required />
    </div>
  </div>
  <div class="word_list-container">
    <div>Word List</div>
    <div>
      Between 10 and 30 words. Puzzles are randomly generated using a selection
      of your words at play time.
    </div>
    <div class="table-container">
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
    </div>
  </div>
  <div class="btnOrange-container">
    <button class="btnPush btnOrange">Submit</button>
  </div>
</main>
<footer>
  <div class="instructions">
    <div>
      Instructions
    </div>
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
