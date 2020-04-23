$mealForm = $('#send-ids');
$searchList = $('#search-list');
$mealList = $('#meal-list');

SELECTED_FOODS = [];

BASE_URL = `${location.origin}/meal/api`

// clear send-ids form values
for (let i=0; i<4; i++){
    
    let input = $mealForm.children();

    $(input[i]).val('');
}

async function handlesubmit(evt){
    evt.preventDefault();

    params = {
        "item": $('#food').val()
    }

    if ($('#brand').val()){
        params["brandOwner"] = $('#brand').val()   
    }

    try{
        let resp = await axios.post(BASE_URL, {params})
        displayResults(resp.data);
    }
    catch(error){
       
        if (error.response.status === 500){

            let btalert = $(`<div class="alert alert-warning" role="alert">
            ${error.response.data.error}
          </div>`)
          $('#top').prepend(btalert);
        }
    }
}

function displayResults(resp){
    $searchList.empty();
    $('#directions').empty();
    $('#directions').append('<div>Click on an ingredient to add it to your meal</div>');
    for (food of resp){
        let $item = $(`<li class="list-group-item" data-id=${food.fdcId}>${food.description}<br>
            <small class="text-muted" data-id=${food.fdcId}>${food.ingredients}</small><br>
            ${food.brandOwner}</li>
            `)
        $searchList.append($item);
        }
}

function selectFood(evt){
    
    if (SELECTED_FOODS.length < 4){
        if (evt.target.tagName === 'LI') {
            $item = $(evt.target);
        }
        else{
            $item = $(evt.target).parent();
        }

        //add color and spacing
        $item.addClass('my-1 rounded').css('background-color', 'rgb(245, 235, 181)');
        //add to my ingredients
        $item.append('<i class="fas fa-trash m-1"></i>');
       

        $mealList.append($item);
        //add id to list
        SELECTED_FOODS.push($item.attr('data-id'));
    }
}

function deleteFood(evt){
    $item = $(evt.target).parent();
 
    //remove from selected_foods array
    i = SELECTED_FOODS.findIndex(val => {
        return val === $item.attr('data-id');
    })

    SELECTED_FOODS.splice(i,1);
    
    $item.remove();
}

function addFoodIds(evt){
   
    // stop form from submitting for now
    evt.preventDefault();

    //add values to form inputs
    for (let i=0; i<SELECTED_FOODS.length; i++){

        let input = $mealForm.children();

        $(input[i]).val(SELECTED_FOODS[i]);
    }

    $mealForm[0].submit();
}

$mealForm.on('submit', addFoodIds);
$('#search').on('submit', handlesubmit);
$searchList.on('click', 'li', selectFood);
$mealList.on('click', 'i', deleteFood);