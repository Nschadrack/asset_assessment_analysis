window.onload=function(){
    var car_title_header_button_clicked = document.getElementById("car_title_header_and_new_btn_button");
    // var cancelOperation = document.getElementById("cancel_operation");
    var groupCarRegisterForm = document.getElementById("car_new_form");

    /* Group car page function call */
    car_title_header_button_clicked.addEventListener('click', showNewGroupCarRegiseterForm);
    // cancelOperation.addEventListener('click', showGroupCarList);
}

/* javascript for group car page */
function showNewGroupCarRegiseterForm(e){
    var form_div_to_show = document.getElementById("car_new_form_div");
    var car_list_to_hide = document.getElementById("car_table_data");
    var car_title_header_button_clicked = document.getElementById("car_title_header_and_new_btn_button");
    var car_title_header_paragraph = document.getElementById("car_title_header_and_new_btn_p");

    form_div_to_show.style.display="block";
    car_list_to_hide.style.display = "none";
    car_title_header_button_clicked.style.display="none";
    car_title_header_paragraph.style.display="none";
}
function showUserRegistrationForm(e){
    var user_login_form = document.getElementById("login-form");
    var user_register_form = document.getElementById("registration-form");

    user_login_form.style.display="none";
    user_register_form.style.display = "block";
}

function toggleAssetRegistrySection(e){
    var assets_registry_section = document.getElementById("assets-registry-section");
    var style = window.getComputedStyle(assets_registry_section);
    var displayCss = style.getPropertyValue("display")
    if (displayCss === "none"){
        assets_registry_section.style.display = "block";
    }else{
        assets_registry_section.style.display = "none";
    }
    
}

function toggleAssetsConsolidationSection(e){
    var assets_consolidation_section = document.getElementById("assets-consolidation-section");
    var style = window.getComputedStyle(assets_consolidation_section);
    var displayCss = style.getPropertyValue("display")
    if (displayCss === "none"){
        assets_consolidation_section.style.display = "block";
    }else{
        assets_consolidation_section.style.display = "none";
    }
}

function toggleUsersManagementAssetSection(e){
    var users_management_section = document.getElementById("users-management-section");
    var style = window.getComputedStyle(users_management_section);
    var displayCss = style.getPropertyValue("display")
    if (displayCss === "none"){
        users_management_section.style.display = "block";
    }else{
        users_management_section.style.display = "none";
    }
}


