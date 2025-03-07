
def create_card(title, value, width="120px", height="60px", 
                title_color="white", value_color="white", 
                title_font_size="18px", value_font_size="28px", 
                value_font_weight="bold", background_gradient_start="#1b4e57", 
                background_gradient_end="#4fb1ad", padding="20px"):
    """
    Function to create a card with a title and value, allowing customization of styles.
    
    Args:
    - title (str): The title of the card (e.g., "Total Rows").
    - value (str/int/float): The value to display inside the card.
    - width (str): The width of the card (default is '250px').
    - height (str): The height of the card (default is '150px').
    - title_color (str): Color of the title text (default is 'white').
    - value_color (str): Color of the value text (default is 'white').
    - title_font_size (str): Font size of the title (default is '18px').
    - value_font_size (str): Font size of the value (default is '28px').
    - value_font_weight (str): Font weight of the value text (default is 'bold').
    - background_gradient_start (str): Start color of the gradient background (default is '#1b4e57').
    - background_gradient_end (str): End color of the gradient background (default is '#4fb1ad').
    - padding (str): Padding inside the card (default is '20px').
    
    Returns:
    - str: HTML string to render the card.
    """
    
    card_html = f"""
    <div style="background: linear-gradient(135deg, {background_gradient_start}, {background_gradient_end}); 
                padding: {padding}; 
                border-radius: 12px; 
                text-align: center; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                width: {width};  /* Set the width of the card */
                height: {height}; /* Set the height of the card */
                min-height: {height}; /* Ensure minimum height */
                display: flex;        /* Use flexbox for content alignment */
                justify-content: center;  /* Center content vertically */
                align-items: center;  /* Center content horizontally */
                margin: 0 auto;  /* Center the card horizontally */
                overflow: hidden;  /* Handle any overflow of content */
                ">
        <div>
            <h3 style="color: {title_color}; font-size: {title_font_size};">{title}</h3>
            <p style="color: {value_color}; font-size: {value_font_size}; font-weight: {value_font_weight};">{value}</p>
        </div>
    </div>
    """
    return card_html