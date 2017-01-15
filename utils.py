from gensim.models import Word2Vec

class Music2Vec(object):
	def __init__(self, size='complete', split='train'):
		self.tags_lut = {}
		self.songs_lut = {}
		self.uuid = None
		self.corpus = None
		self.appearances = None
		self.MIN_SONGS = 10

		self.get_data(size, split)
		self._create_hashes(size)

	def get_data(self, size, split):
		fpath = 'data/yes_'+size+'/'+split+'.txt'
		with open(fpath, 'r') as f:
			mydata = f.read()

		r_uuid, r_appearances, r_corpus = mydata.split('\n', 2)
		self.uuid = map(int, r_uuid.split())
		self.appearances = map(int, r_appearances.split())
		self.corpus = [plist.split() for plist in r_corpus.split('\n')]
		print 'Loading the {} data from the {} dataset'.format(split, size)

	def _create_hashes(self, size):
		tag_fpath = 'data/yes_'+size+'/tag_hash.txt'
		song_fpath = 'data/yes_'+size+'/song_hash.txt'

		with open(song_fpath, 'r') as f:
			songs = [line.strip('\n').replace('w\\/', 'feat.').split('\t') for line in f.readlines()]

		self.songs_lut = {int(idx): {'artist': artist, 'song': song} for idx, song, artist in songs}

		with open(tag_fpath, 'r') as f:
			tags  = map(lambda x: x.split(', '), map(lambda x: x.strip('\n'), f.readlines()))

		self.tags_lut = {idx: tag for idx, tag in tags}

	def clean_song2vec(self):
		return filter(lambda x: len(x) > self.MIN_SONGS, self.corpus)

	def clean_artist2vec(self):
		idx2artist = [map(lambda x: self.songs_lut[int(x)]['artist'], pl) for pl in self.corpus]
		return filter(lambda x: len(x) > self.MIN_SONGS, idx2artist)

def main():
	mtv = Music2Vec()
	corpus = mtv.clean_artist2vec()
	# fpath = 'artist2vec_model.pkl'
	# model = Word2Vec(corpus, seed=1738)
	# model.save(fpath)
	# print 'Model saved to {}'.format(fpath)
	# model = Word2Vec.load(fpath)

if __name__ == '__main__':
	main()
