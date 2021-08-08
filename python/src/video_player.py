"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._yt_playlist = {} #Youtube playlist
        self._video_state = 0   #Where 0 = Not playing, 1 = Playing, 2 = Pause
        self._stored_video = None   #Stores video if not none


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        for vid in sorted(all_videos, key= lambda x: x.title):
            print(vid)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        vid = self._video_library.get_video(video_id)
        if vid is None:
            print("Cannot play video: Video does not exist")
            return
        if self._video_state == 1:
            print(f"Stopping video: {self._stored_video.title}")
        if self._video_state == 2:
            print(f"Stopping video: {self._stored_video.title}")
        print(f"Playing video: {vid.title}")
        self._stored_video = vid
        self._video_state = 1
        return

    def stop_video(self):
        """Stops the current video."""

        if self._video_state == 0:
            print("Cannot stop video: No video is currently playing")
            return
        if self._video_state == 1 or 2:
            print(f"Stopping video: {self._stored_video.title}")
            self._video_state = 0
            self._stored_video = None
            return

    def play_random_video(self):
        """Plays a random video from the video library."""

        if self._video_state ==1:
            print(f"Stopping video: {self._stored_video.title}")
        vid = random.choice(self._video_library.get_all_videos())
        print(f"Playing video: {vid}")
        self._stored_video = vid
        self._video_state = 1

    def pause_video(self):
        """Pauses the current video."""
        if self._video_state == 0:
            print("Cannot pause video: No video is currently playing")
            return
        if self._video_state == 2:
            print(f"Video already paused: {self._stored_video.title}")
            return
        if self._video_state == 1:
            print(f"Pausing video: {self._stored_video.title}")
            self._video_state = 2 #means pause
            return


    def continue_video(self):
        """Resumes playing the current video."""
        if self._video_state == 1:
            print("Cannot continue video: Video is not paused")
            return
        if self._video_state == 2:
            print(f"Continuing video: {self._stored_video.title}")
            self._video_state = 1
            return
        if self._video_state == 0:
            print("Cannot continue video: No video is currently playing")
            return


    def show_playing(self):
        """Displays video currently playing."""

        if self._video_state ==0:
            print("No video is currently playing")
            return
        if self._video_state ==1:
            print(f"Currently playing: {self._stored_video}")
            return
        if self._video_state ==2:
            print(f"Currently playing: {self._stored_video}{' - PAUSED' if self._video_state ==2 else ''}")
            return

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        if name not in self._yt_playlist:
            print(f"Successfully created new playlist: {playlist_name}")
            self._yt_playlist[name] = Playlist(playlist_name)  # Playlist added in class
            return
        elif name in self._yt_playlist:
            print("Cannot create playlist: A playlist with the same name already exists")


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        name = playlist_name.lower()
        vid = self._video_library.get_video(video_id)
        if name not in self._yt_playlist:
            print("Cannot add video to another_playlist: Playlist does not exist")
            return
        if vid is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return
        if vid in self._yt_playlist[name].videos:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return
        self._yt_playlist[name].videos.append(vid)
        print(f"Added video to {playlist_name}: {vid.title}")

        #print(f"Would you like to see the added video? {self.show_playlist if input() ==1 else ''}" )
        #return


    def show_all_playlists(self):
        """Display all playlists."""

        if not self._yt_playlist:
            print("No playlists exist yet")
            return
        print(f"Showing all playlists:")
        for each in sorted(self._yt_playlist):
            print(self._yt_playlist[each].playlist)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._yt_playlist:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return
        print(f"Showing playlist: {playlist_name}")
        if not self._yt_playlist[playlist_name.lower()].videos:
            print("No videos here yet")
            return
        for each in self._yt_playlist[playlist_name.lower()].videos:
            print(each)


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        name = playlist_name.lower()
        if name not in self._yt_playlist:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        vid = self._video_library.get_video(video_id)               #Getting video object using video_id
        playlist_vid = self._yt_playlist[name].videos      #Getting all video objects in playlist
        #print(vid)
        if not playlist_vid:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return
        if vid not in playlist_vid:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        elif vid in playlist_vid:            #Check if video object present in playlist, then remove
            playlist_vid.remove(vid)
            print(f"Removed video from {playlist_name}: {vid.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        if name not in self._yt_playlist:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self._yt_playlist[name].videos = []
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        if name not in self._yt_playlist:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        else:
            self._yt_playlist.pop(name) #Change
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        searched = []
        _search = search_term.lower()  #cat
        video_list = self._video_library.get_all_videos()   #list of videos
        for vid in video_list:
            if _search in vid.title.lower():
                 searched.append(vid)

        if not searched:        #Check if empty
            print(f"No search results for {search_term}")
            return
        else:
            searched = sorted(searched, key= lambda x: x.title)
            print(f"Here are the results for {search_term}:")
            for index, v in enumerate(searched, start=1):
                print(f"{index}) {v}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            i = input()
            if i.isnumeric() and 1<=int(i)<= len(searched):     #Check is input is a valid number
                self.play_video(searched[int(i)-1].video_id)    #Play video


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        searched =[]
        _search = video_tag.lower()
        video_list = self._video_library.get_all_videos()
        for vid in video_list:
            if _search in vid.tags:
                searched.append(vid)

        if not searched:
            print(f"No search results for {video_tag}")
            return
        else:
            searched = sorted(searched, key = lambda x: x.title)
            print(f"Here are the results for {video_tag}:")
            for index, v in enumerate(searched, start=1):
                print(f"{index}) {v}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            i = input()
            if i.isnumeric() and 1<= int(i) <= len(searched):
                self.play_video(searched[int(i)-1].video_id)





