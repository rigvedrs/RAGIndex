css = """
<style>
/* Common styles for all chat messages */
.chat-message {
  padding: 1rem 1.5rem;
  border-radius: 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: flex-start; /* Align items to the top */
  max-width: 60%; /* Slightly reduced max-width */
  align-self: flex-start; /* Default alignment */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Add a subtle box shadow */
}

/* Differentiating colors for user and bot messages */
.chat-message.user {
  background-color: #475063; /* Updated background color */
  margin-left: auto; /* Pushes the chat box to the right side */
  margin-right: 0;
}

.chat-message.bot {
  background-color: #2b313e; /* Updated background color */
  margin-left: 0;
  margin-right: auto; /* Pushes the chat box to the left side */
}

/* Avatar styling */
.chat-message .avatar {
  width: 15%; /* Reduced avatar width */
  flex-shrink: 0; /* Prevents the avatar from shrinking if message content is too long */
}

.chat-message .avatar img {
  width: 100%; /* Ensures the image takes the full width of its container */
  max-width: 3vw; /* Reduced responsive max-width */
  max-height: 3vw; /* Reduced responsive max-height */
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff; /* Add a white border around the avatar */
}

/* Message content styling */
.chat-message .message {
  width: 80%; /* Increased message width */
  padding: 0 1rem; /* Reduced padding */
  color: #fff;
  word-wrap: break-word; /* Breaks long words to ensure they don't overflow the container */
  font-size: 0.9rem; /* Slightly reduced font size */
  line-height: 1.4; /* Increased line-height for better readability */
}

/* Responsive design adjustments */
@media (max-width: 768px) {
  .chat-message .avatar img {
    max-width: 40px;
    max-height: 40px;
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
