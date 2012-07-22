function validateForm()
{
    var n = document.forms["register"]["name"].value;
    var s = document.forms["register"]["last-name"].value;
    var e = document.forms["register"]["email"].value;
    if (n==null || n=="" || s==null || s=="" || e==null || e=="")
    {
          alert("Debe completar: Nombre, Apellido y Email");
          return false;
    }
}
