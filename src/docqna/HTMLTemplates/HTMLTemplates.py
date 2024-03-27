css = """
<style>
/* Common styles for all chat messages */
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center; /* For vertical alignment of children */
    max-width: 70%; /* Limit width for better appearance */
    align-self: flex-start; /* Default alignment */
}

/* Differentiating colors for user and bot messages */
.chat-message.user {
    background-color: #2b313e;
    margin-left: auto; /* Pushes the chat box to the right side */
    margin-right: 0;
}
.chat-message.bot {
    background-color: #475063;
    margin-left: 0;
    margin-right: auto; /* Pushes the chat box to the left side */
}

/* Avatar styling */
.chat-message .avatar {
    width: 20%;
    flex-shrink: 0; /* Prevents the avatar from shrinking if message content is too long */
}
.chat-message .avatar img {
    width: 100%; /* Ensures the image takes the full width of its container */
    max-width: 5vw; /* Responsive max-width */
    max-height: 5vw; /* Responsive max-height */
    border-radius: 50%;
    object-fit: cover;
}

/* Message content styling */
.chat-message .message {
    width: 75%; /* Reduced a bit to avoid potential overflow issues */
    padding: 0 1.5rem;
    color: #fff;
    word-wrap: break-word; /* Breaks long words to ensure they don't overflow the container */
}

/* Responsive design adjustments */
@media (max-width: 768px) {
    .chat-message .avatar img {
        max-width: 60px;
        max-height: 60px;
    }
}
</style>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://w7.pngwing.com/pngs/321/395/png-transparent-popeye-the-sailor-man-popeye-village-sweepea-popeye-the-sailor-cartoon-popeye-comics-child-hand-thumbnail.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://w7.pngwing.com/pngs/321/395/png-transparent-popeye-the-sailor-man-popeye-village-sweepea-popeye-the-sailor-cartoon-popeye-comics-child-hand-thumbnail.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""
