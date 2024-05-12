<script>
  import Nav from "../components/Nav.svelte";

  const url = 'http://localhost:8000/ping';

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Server responded with:', data);
  })
  .catch(error => {
    console.error('There was a problem with the request:', error);
  });

</script>

<Nav location="home"></Nav>
<main>

</main>
<footer></footer>