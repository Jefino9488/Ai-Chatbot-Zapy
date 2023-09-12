# # Step1 Create an account or log in to your Spotify Developers account "https://developer.spotify.com/dashboard/login".
# # Step 2: Create an App.
# # Step 3: The dashboard would be opened. Now, Save your Client Id, Client Secret, this will be used later in our program.
# # Step 4: Click on the “EDIT SETTING” button and add in the Redirect URIs as follow.
# # http://google.com/callback/
# # Step 5: Click on add and save the changes.
# # Step 6: Now past your username(to know ur username https://www.spotify.com/us/account/overview/), clientID, clientSecret
# import spotipy
# import webbrowser
#
# username = 'YOURS_HERE'
# clientID = 'YOURS_HERE'
# clientSecret = 'YOURS_HERE'
# redirect_uri = 'http://google.com/callback/'
# oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
# token_dict = oauth_object.get_access_token()
# token = token_dict['access_token']
# spotifyObject = spotipy.Spotify(auth=token)
# user_name = spotifyObject.current_user()
#
#
# def songv():
#     search_song = input("Enter the song name: ")
#     results = spotifyObject.search(search_song, 1, 0, "track")
#     songs_dict = results['tracks']
#     song_items = songs_dict['items']
#     song = song_items[0]['external_urls']['spotify']
#     webbrowser.open(song)
#     print('Song has opened in your browser.')
#
#
# def song(user_input):
#     search_song = user_input
#     results = spotifyObject.search(search_song, 1, 0, "track")
#     songs_dict = results['tracks']
#     song_items = songs_dict['items']
#     song = song_items[0]['external_urls']['spotify']
#
#     webbrowser.open(song)
#     print('Song has opened in your browser.')
