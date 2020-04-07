$mealForm = $('#send-ids')
$searchList = $('#search-list')

SELECTED_FOODS = []

BASE_URL = `http://${location.host}/meal/api`

// clear send-ids form values
for (let i=0; i<4; i++){
    
    let input = $mealForm.children()

    $(input[i]).val('')
}

async function handlesubmit(evt){
    evt.preventDefault()

    params = {
        "query": $('#food').val(),
        "requireAllWords": true,
        "dataType": "Branded"
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

        let input = $mealForm.children()

        $(input[i]).val(SELECTED_FOODS[i])
    }

    $mealForm[0].submit()
}

$mealForm.on('submit', addFoodIds)
$('#search').on('submit', handlesubmit)
$searchList.on('click', 'li', selectFood)