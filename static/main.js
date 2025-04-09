const apiUrl = "http://localhost:8000/calories/";
let dailyTarget = 0; //tracks the daily calorie target
let editingFoodId = null; //tracks which food item is being edited

//fetches calorie data from the backend
async function fetchCalories() {
    const response = await fetch(apiUrl);
    const data = await response.json();
    const totalCalories = data.totalCalories;
    document.getElementById('totalCalories').textContent = totalCalories;

    //calculates and display the percentage of the daily target
    if (dailyTarget === 0) {
        document.getElementById('caloriePercentage').textContent = "Set a target to see percentage";
    } else {
        const percentage = ((totalCalories / dailyTarget) * 100).toFixed(2);
        document.getElementById('caloriePercentage').textContent = percentage + "%";
    }

    //displays the list of logged food items
    const foodList = document.getElementById('foodList');
    foodList.innerHTML = '';
    data.foods.forEach((food, index) => {
        const li = document.createElement('li');
        li.innerHTML = `<b>${food.name}</b> ${food.calories} Calories`;

        //adds Edit button
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.classList.add('edit');
        editButton.onclick = () => editFood(index, food.name, food.calories);
        li.appendChild(editButton);

        //adds delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.classList.add('delete');
        deleteButton.onclick = () => deleteFood(index);
        li.appendChild(deleteButton);

        foodList.appendChild(li);
    });
}

//sets the daily calorie target
async function setCalorieTarget() {
    dailyTarget = document.getElementById('calorieTarget').value;
    if (dailyTarget > 0) {
        await fetch(apiUrl + 'target', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target: Number(dailyTarget) })
        });
        fetchCalories();
    } else {
        alert("Please enter a valid calorie target.");
    }
}

//logs a new food item or update an existing one
async function logFood() {
    if (dailyTarget === 0) {
        alert("Please set a daily calorie target before logging food.");
        return;
    }

    let name = document.getElementById('foodName').value;
    name = name.charAt(0).toUpperCase() + name.slice(1);
    
    const calories = document.getElementById('foodCalories').value;

    if (editingFoodId !== null) {
        //if editing it sends a PUT request to update the food item
        await updateFood(editingFoodId, name, calories);
        editingFoodId = null; // Reset editing state
    } else {
        //if it is not editing, send a POST request to log a new food item
        const response = await fetch(apiUrl + 'log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, calories: Number(calories) })
        });

        if (!response.ok) {
            alert("Failed to log food");
            return;
        }
    }

    document.getElementById('foodForm').reset();
    fetchCalories();
}

//update an existing food
async function updateFood(index, name, calories) {
    const response = await fetch(apiUrl + `log/${index}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, calories: Number(calories) })
    });

    if (!response.ok) {
        alert("Failed to update food");
    }
}

//deletes  food item
async function deleteFood(index) {
    const response = await fetch(apiUrl + `log/${index}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        fetchCalories();
    } else {
        alert("Failed to delete food");
    }
}

//populates the form with a food item's data for editing
function editFood(index, name, calories) {
    document.getElementById('foodName').value = name;
    document.getElementById('foodCalories').value = calories;
    editingFoodId = index; //sets the editing state
}

//loads calorie data on page load
fetchCalories();
