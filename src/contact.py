"""

Simply handle a contact form request and send an email.

"""

import webapp2

import json

from google.appengine.api import mail


SEND_TO_ADDRESS = 'cit@cittech.co'
SEND_FROM_ADDRESS = 'contact@cittech-co.appspotmail.com'


class ContactFormRequestHandler(webapp2.RequestHandler):
	def post(self):
		""" Take the contact form and send an email. """
		request_object = json.loads(self.request.body)
		response_object = {}
		if not request_object:
			self.abort(400)
		name = request_object.get('name', False)
		if not name:
			self.abort(400)
		email = request_object.get('email', False)
		if not email:
			self.abort(400)
		if not mail.is_email_valid(email):
			self.abort(400)
		message = request_object.get('message', False)
		if not message:
			self.abort(400, detail='No message value supplied.')

		mail.send_mail(
			SEND_FROM_ADDRESS,
			SEND_TO_ADDRESS,
			'CiT Tech Web Form',
			''.join([
				'Name: ',
				name,
				'\n',
				'Email: ',
				email,
				'\n',
				'Message:\n',
				message
			])
		)

		response_object['email'] = email
		response_object['name'] = name
		response_object['message'] = message

		self.response.content_type = 'application/json'
		self.response.out.write(json.dumps(response_object))


APP = webapp2.WSGIApplication([
	webapp2.Route(
		'/api/contact',
		handler=ContactFormRequestHandler,
		methods=['POST']
	)
])
