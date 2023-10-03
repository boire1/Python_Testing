Issue n° 1
ERROR: Entering a unknown email crashes the app 

The  encountering came from this line:
club = [club for club in clubs if club['email'] == request.form['email']][0]


`If the email isn't found, the list comprehension will return an empty list, and trying to get the first element of an empty list with [0] will cause an IndexError.

To fix this, I checked if the email exists in the clubs, and if not, displayed a relevant error message.      `

What i did

    1.Removed the [0] from the list comprehension to avoid an immediate error.
    2.Checked if the list club_list is empty. If it's empty, flashed the error message and redirected the user to the index page.
    3.If the list isn't empty (i.e., the email was found), the first item in the list is assigned to the club variable and the   rest of the code proceeds as before.

2. Modify index.html
    (to display flashed messages:)
    
` {% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
      {% for message in messages %}
        <li>{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

    `