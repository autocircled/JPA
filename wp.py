# Get help from https://gist.github.com/autocircled/e2271aa3da7b7dd7a2be4b55d38e3f0b

# import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from datetime import datetime
# import os

class Custom_WP_XMLRPC:
	def post_article( self, wpUrl, wpUserName, wpPassword, jobTitle, slug, jobPublishDate, jobExcerpt, jobDescription, status, company, all_locations, job_natures, job_industries, job_type, job_location_type, post_meta ):
		self.wpUrl = wpUrl
		self.wpUserName = wpUserName
		self.wpPassword = wpPassword
		
		#Upload to WordPress
		client = Client( self.wpUrl, self.wpUserName, self.wpPassword )
		
		#Post
		post = WordPressPost()
		post.title = jobTitle
		post.slug = slug
		post.date = jobPublishDate
		post.excerpt = jobExcerpt
		post.content = jobDescription
		post.terms_names = { 'location': all_locations,'company': company, 'job_nature': job_natures, 'job_industry': job_industries, 'job_type': job_type, 'job_location_type': job_location_type }
		post.post_status = status
		post.custom_fields = post_meta
		post.post_type = 'jobs'
		post.id = client.call( posts.NewPost(post) )

		now = datetime.now()
		cdt= now.strftime("%Y-%m-%d %H:%M:%S") # Current date and time
		print('Published - ' + cdt,' :: ',post.id, '-', post.title)
		return post.id
