<script>
    let { data } = $props()
    console.log(data)
</script>

<ul>
    {#each data.articles as article}
    <li>
        {article.title}; retrieved on {article.time_scraped}
    </li>
    {/each}
</ul>
