<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>
    <link rel="stylesheet" href="../css/contact.css">
    <link rel="stylesheet" href="../css/navbar-container.css">
</head>
<body>
    <div class="navbar-container">
        <nav>
            <div class="logo">
                <a href="#">Logo</a>
            </div>
            <ul class="menu">
                <li><a href="homepage.html">Home</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="contact.html">Contact</a></li>
                <li><a href="career.html">Careers</a></li>
            </ul>
        </nav>
    </div>

    <div class="contact-container">
        <div class="contact-frame">
            <div class="title"> Contact Us</div>
            <div class="subtitle"> Have business inquiries or questions? You can send a message here and our team will get back to you as soon as possible!</div>
    
            <form method="post" action="comment.php">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br>
    
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required><br>
    
                <label for="organization">Organization:</label>
                <input type="text" id="organization" name="organization"><br>
    
                <label for="role">Role:</label>
                <input type="text" id="role" name="role"><br>
    
                <label for="subject">Subject:</label>
                <input type="text" id="subject" name="subject" required><br>
    
                <label for="problem">Problem:</label>
                <textarea id="problem" name="problem" rows="4" required></textarea><br>
    
                <button type="submit">Submit</button>
               

            </form>
        </div>
        <div class="confirmation-container" id="confirmation-container">
        <div class="confirmation-message" id="confirmation-message">
            Thank you for submitting! We will help you solve it soon.
        </div>
    </div>

    <div class="confirmation-message" id="confirmation-message">
                Thank you for submitting! We will help you solve it soon.
            </div>
        
        <script>
            document.addEventListener("DOMContentLoaded", function () {
                const form = document.querySelector("form");
                const confirmationMessage = document.getElementById("confirmation-message");
        
                form.addEventListener("submit", function (e) {
                    e.preventDefault(); 
                    confirmationMessage.style.display = "block";
                    form.reset();
                });
            });
        </script>
        
            
        
    </div>

</body>
</html>
