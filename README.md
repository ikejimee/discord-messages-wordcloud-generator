# Discord-Data-Package-Message-Wordcloud-Generator
Web page that generates a wordcloud based on messages from your discord data package. 


# How to use
1. Request a copy of your discord data (Discord may take up to 30 days to email this). Further instructions are here https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data
  
3. Clone the Repository
   git clone https://github.com/ikejimee/Discord-Data-Package-Message-Wordcloud-Generator.git
   cd Discord-Data-Package-Message-Worldcloud-Generator
4. Install Dependencies
   ```bash
   pip install -r requirements.txt
6. Run the Flask App
   ```bash
   python app.py
8. Open the web app in browser
   ```bash
   http://127.0.0.1:5000
10. Upload your discord data package zip file to the web app
11. Wait for the wordcloud to generate and enjoy!

# Further Improvements
1. Allow users to download a .png file of the wordcloud
2. Allow users to customise features of the wordcloud (eg: colour)
3. Allow users to request their wordcloud based on a specific date range
