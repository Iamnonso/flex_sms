//if candidate select the state of origin
const selectState = document.getElementById('stud_state');
const selectCity = document.getElementById('stud_city');

selectState.addEventListener('change', (event) => {
    event.preventDefault();
    const state = selectState.value;
    selectCity.innerHTML = '<option value="">Please wait...</option>';
    $.ajax({
        url: `/cities/${state}`,
        type: 'GET',
        success: (data) => {
            const cities = data.response;
            selectCity.innerHTML = '<option value="">Select City</option>';
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.city_name;
                option.textContent = city.city_name;
                selectCity.appendChild(option);
            });
        },

        fail: (error) => {
            selectCity.innerHTML = '<option value="">Select City</option>';
            console.log(error);
        }
    });
});

//handle health checkbox
const healthCheck = (health) => {
    const healthStatement = document.getElementById('healthconditionstatement');
    if (health == 'True') {
        healthStatement.toggleAttribute('enabled');
    }
    console.log(health);
}

personalData = () => {
    const form = document.getElementById('personaldata');
    const formData = new FormData(form);
    const formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });
    return formObject;
}