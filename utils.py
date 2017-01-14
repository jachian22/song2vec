

def get_data(size='small', split='train'):
	fpath = 'data/yes_'+size+'/'+split+'.txt'
	with open(fpath, 'r') as f:
		mydata = f.read()

	r_uuid, r_appearances, r_playlists = mydata.split('\n', 2)
	c_uuid        = map(int, r_uuid.split())
	c_appearances = map(int, r_appearances.split())
	c_playlists   = [plist.split() for plist in r_playlists.split('\n')]
	print 'Loading the {} data from the {} dataset'.format(split, size)
	return c_uuid, c_appearances, c_playlists

def create_hashes(size='small'):
	song_fpath = 'data/yes_'+size+'/song_hash.txt'
	tag_fpath  = 'data/yes_'+size+'/tag_hash.txt'

	with open(song_fpath, 'r') as f:
		songs = [line.strip('\n').replace('w\\/', 'feat.').split('\t') for line in f.readlines()]

	songs_lut = {int(idx): {'artist': artist, 'song': song} for idx, song, artist in songs}

	with open(tag_fpath, 'r') as f:
		tags = map(lambda x: x.split(', '), map(lambda x: x.strip('\n'), f.readlines()))

	tags_lut = {int(idx): tag for idx, tag in tags}
	return songs_lut, tags_lut # remove later

def clean_song2vec(playlist):
	MIN_SONGS = 10
	return filter(lambda x: len(x) > MIN_SONGS, playlist)