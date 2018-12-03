#!/usr/bin/python3

import math
import numpy             as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

	length     = 50000;

	## PoCo proposition
	f          = 3;
	minscore   = 3*f;
	transition = lambda s, f, b: s+1 if b else math.floor(s*(f-1)/f)+1

	## BAD!
	# f          = 0.2
	# minscore   = 1;
	# transition = lambda s, f, b: s+1 if b else (s+1)/6

	## SARMENTA
	# f          = 0.2;
	# minscore   = 1;
	# transition = lambda s, f, b: s+1 if b else 0

	fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(16,9))
	ax1.set_title('Score dynamics (f={:.0%})'.format(f))
	ax1.set_xlim(0, length)
	ax1.set_yscale('log')
	ax2.set_yscale('log')
	ax1.set_ylabel("Score")
	ax2.set_ylabel("Estiamted error rate")
	ax2.set_xlabel('Number of contributions')

	for reliability in [0.9, 0.99, 0.999, 0.9999]:
		# for _ in range(5):

			contribs = np.random.random(length) < reliability
			score    = np.zeros(length+1)

			for i in np.arange(length):
				score[i+1] = transition(score[i], f, contribs[i])

			ax1.plot(score, label="reliability {0:.2%}".format(reliability))
			ax2.plot(f/np.maximum(score, minscore))

	fig.legend(loc='right', shadow=True)
	plt.show()
