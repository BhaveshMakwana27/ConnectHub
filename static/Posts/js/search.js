searchPost = document.getElementById('searchPosts')
searchPeople = document.getElementById('searchPeople')

if (searchPost.hidden==false && searchPeople.hidden==false){
    searchPost.hidden=true
}

filterPeopleBtn = document.getElementById('filter-people')
filtePostBtn = document.getElementById('filter-post')

filterPeopleBtn.onclick = ()=>{
    searchPost.hidden = true
    searchPeople.hidden = false
}
filtePostBtn.onclick = ()=>{
    searchPeople.hidden = true
    searchPost.hidden = false
}


// Handle Likes 
$('.like-form').submit(function (e) {
    const post_id = $(this).attr('id')
    const url = this.action
    let likeBtn = document.getElementById('likeButton' + post_id)
    let count_like = document.getElementById('likes_count' + post_id)
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id': post_id
        },
        encode: true
    }).done((data) => {
        like_status = JSON.parse(data)['like_status']
        totalLikes = Number.parseInt(count_like.innerText)
        if (like_status == false) {
            totalLikes -= 1
            if (totalLikes==0){
                count_like.hidden=true
                count_like.innerHTML = '0'
            }else{
                count_like.innerHTML = `<i class='bi bi-hand-thumbs-up-fill' style='color:#0000ffbd'></i> ${totalLikes}`
            }
            likeBtn.innerHTML = `<i class="bi bi-hand-thumbs-up"></i> Like`
        } else {
            count_like.hidden = false
            totalLikes += 1
            count_like.innerHTML = `<i class='bi bi-hand-thumbs-up-fill' style='color:#0000ffbd'></i> ${totalLikes}`
            likeBtn.innerHTML = `<i class="bi bi-hand-thumbs-up-fill"></i> Liked`
        }
    })
    e.preventDefault()
})
