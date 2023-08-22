$(window).on('resize',function(){
    filterCollapse()
})
filterCollapse()
function filterCollapse(){
    let width = window.innerWidth
    let filters = document.getElementById('filters')
    let filterCollapse = document.getElementById('collapseFilter')
    if (width<992){
        filters.hidden = true
        filterCollapse = false
    }else{
        filters.hidden = false
        filterCollapse = true

    }
}


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






