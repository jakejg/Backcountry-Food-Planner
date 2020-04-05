$('#search').on('submit', handlesubmit)
$('#send-ids').on('submit', addFoodIds)

$searchList = $('#search-list')
$searchList.on('click', 'li', selectFood)
SELECTED_FOODS = []

BASE_URL = `http://${location.host}/meal/api`

async function handlesubmit(evt){
    evt.preventDefault()

    params = {
        "query": $('#food').val(),
        "requireAllWords": true,
        "dataType": "SR, Legacy, Branded, Foundation"
    }

    if ($('#brand').val()){
        params["brandOwner"] = $('#brand').val()   
    }

    try{
        let resp = await axios.post(BASE_URL, {params})
        console.log(resp)
        displayResults(resp.data)
    }
    catch(error){
    
    }
}

function displayResults(resp){
    $searchList.empty()
    for (food of resp.foods){
        $item = $(`<li class="list-group-item" data-id=${food.fdcId}>${food.description}<br>
            <small class="text-muted" data-id=${food.fdcId}>${food.ingredients}</small></li>`)
        $searchList.append($item)
        }
}

function selectFood(evt){
    
    if (SELECTED_FOODS.length < 4){
        //add color
        $(evt.target).addClass('bg-info')
        //add to my ingredients
        $('#meal-list').append($(evt.target))
        //add id to list
        SELECTED_FOODS.push($(evt.target).attr('data-id')) 
    }

    console.log(SELECTED_FOODS)
}

function addFoodIds(evt){
   
    // stop form from submitting for now
    evt.preventDefault()

    //add values to form inputs
    for (let i=0; i<SELECTED_FOODS.length; i++){
        $( `#send-ids input:nth-child(${i+1})`).val(SELECTED_FOODS[i])
    }
    
    $('#send-ids')[0].submit()

}