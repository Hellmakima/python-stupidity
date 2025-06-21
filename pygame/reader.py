import pygame as p

data = """
What is OAuth 2.0?

Gbadebo Bello
September 7, 2023
OAuth 2.0 is an authorization framework that enables users to safely share their data between different applications. It is an industry standard that addresses the API security concerns associated with sharing user credentials while providing simple, well-defined authorization flows for web, mobile, desktop, and IoT applications.

Here, we’ll review the history of OAuth 2.0 before discussing how it works. We’ll then explore some benefits, challenges, and best practices for working with OAuth 2.0—and highlight some features of the Postman API Platform that help simplify OAuth workflows.

What is the history of OAuth 2.0?
Every day, millions of people interact with multiple applications—and share data across them. For instance, someone who uses a fitness app to track their daily workouts may want to start using a new meal planning app to monitor their nutrient intake and calorie consumption. The meal planning app might ask the user to share their data from the fitness app in order to create a more customized experience. While this type of integration has many benefits, it also comes with several security caveats:

User credential exposure: Before OAuth, the user would need to share their username and password for the fitness app with the meal planning app, which would introduce a significant security risk. For instance, the meal planning app might store the user’s credentials in an insecure way, making them vulnerable in the event of a breach.
Scope of access: Before OAuth, the meal planning app might have access to data that the user did not actually wish to share. For instance, the fitness enthusiast in this example might want to share their workout history with the meal planning app, but not their age, email address, occupation, or location.
No way to revoke access: Before OAuth, the user could not easily restrict or revoke the meal planning app’s access to their fitness data. While the user could decide to change their fitness app password, this would affect all of the third-party applications they had previously authorized.
OAuth, which began as a community effort in 2007 and is currently developed and maintained by the Internet Engineering Task Force (IETF), has addressed these challenges through a token-based authorization mechanism. By introducing tokens as a means of granting access, OAuth has eliminated the need for users to share their actual credentials with third-party applications. It also allows users to define specific scopes of access when granting permission, ensuring that applications only accessed the resources they needed. Furthermore, OAuth enables users to explicitly authorize applications for specific actions and revoke access at any time, empowering them to take charge of their data and privacy.

How does OAuth 2.0 work?
Before you can understand how OAuth 2.0 works, you must first understand the four specific roles that are involved in the OAuth 2.0 workflow. Those roles are:

Resource owner: This is the user that is granting third-party access to their data.
Client: This is the third-party application that is requesting access to the resource owner’s data. When the resource owner grants access, the client gets an access token that can be used to request the resources within the granted scope.
Authorization server: The authorization server acts as an intermediary between the client, resource owner, and resource server by issuing access tokens to the client after the resource owner successfully authorizes the request.
Resource server: This is the server that hosts the protected resources. It is responsible for accepting and responding to requests to access protected resources using an access token.
OAuth 2.0 enables the resource owner (i.e., the user) to give the client (i.e., the third-party application) access to their data without having to share their credentials. Instead, the credentials are shared with the authorization server, which issues an access token to the client. The client can then use this access token to get the user’s data from the resource server.

Let’s explore how this works with our example from the previous section. In an OAuth context, the new meal planning application is the client; it wants access to the user’s data from the fitness application. The fitness application has both a resource server and an authorization server that authorizes access to the resource server.

Since the meal planning application is the client, it will present the user with the option to import their fitness history data from the fitness application. If the user decides to proceed, they will be redirected to the fitness application, where they will be prompted to enter their username and password. If the user successfully logs in to the fitness application, they will see a screen where they can review the data that the client would like to access. If the user consents to the requested scope, they will authorize the request. The user will then be redirected back to the meal planning application, where their fitness history from the fitness application will now be visible.

Here is a step-by-step breakdown of everything that happens under the hood:

The client (the meal planning app) asks the user for access to their resources on the resource server of the fitness app.
The user grants access to the client through the authorization server by logging in to the fitness app with their credentials. These credentials are not shared with the client. Instead, an authorization code is generated and shared with the client.
The client uses this authorization code to request an access token from an endpoint that is provided by the authorization server.
The authorization server generates and returns an access token, which the client can use to access the user’s resources on the resource server.
The client sends the access token to the resource server to request access to the user’s resources.
The resource server validates the access token with the authorization server. If the token is valid, it grants the client access to the user’s resources.


What is the difference between access tokens and refresh tokens in OAuth?
As discussed above, the authorization server grants an access token to the client after the user authorizes the request. The client then uses this access token to retrieve the user’s data from the resource server. Access tokens can be stored in different formats, the most common being the JWT (JSON Web Token) format. This format allows the token to contain encrypted data, which can be securely retrieved before the token expires.

Access tokens are often short-lived and therefore need to be re-generated upon expiration. Refresh tokens are used to obtain new access tokens and often have a longer lifespan than access tokens. However, not all OAuth providers issue refresh tokens.

What is an authorization grant, and what are the key types?
An authorization grant is a credential representing the user’s consent to give the client access to its protected resources on the resource server. Once the client receives the grant, it can be exchanged for an access token. OAuth 2.0 defines four primary types of authorization grants:

Authorization code grant
In the example above, we mentioned that the authorization server generates a code and shares it with the client after the user successfully logs in. This code, known as an “authorization code,” is the most secure and common type of authorization grant. It involves a two-step process. First, the client redirects the user to the authorization server, where the user logs in and grants permission. The authorization server then provides an authorization code to the client. In the second step, the client exchanges the authorization code for an access token and, optionally, a refresh token.

Implicit grant
The implicit grant is designed for browser-based applications, such as single-page web apps. In this flow, the access token is returned directly to the client from the authorization endpoint, without going through the authorization code exchange. This simplifies the flow but makes the token more vulnerable to exposure, as it may be logged in the browser’s history or intercepted by malicious actors. It is therefore not recommended and has been deprecated in OAuth 2.0.

Resource owner password credentials (ROPC) grant
In this grant type, the resource owner’s credentials are shared directly with the client, and the client uses these credentials to obtain an access token from the authorization server each time it is needed. Because ROPC involves direct sharing of user credentials, it is less secure and should only be used when the resource owner has a high level of trust in the client.

Client credentials grant
This grant type is used to obtain an access token when a client application (often a server-side application) is requesting access to its own resources. It is appropriate when the client application is the resource owner and it needs access to a protected resource that it owns or controls.

What are the benefits of OAuth 2.0?
OAuth 2.0 offers many benefits that have made it the gold standard for authorization across major tech companies, social media applications, finance applications, and more. These benefits include:

Simplified authorization flow: OAuth 2.0 uses a straightforward authorization flow that is easy to implement, making it more accessible to developers. It uses access tokens for authorization, which makes it scalable and performant in large-scale systems.
Multiple access token types: OAuth 2.0 allows for different types of access tokens, enabling the implementation of various security mechanisms and token lifetimes based on the specific requirements of the applications.
User control: OAuth 2.0 gives users control over their data and the level of access granted to client applications. Users can choose which resources the client application can access, and they can revoke access at any time, enhancing privacy and user trust.
Standardization and broad industry adoption: OAuth 2.0 has been widely adopted by major tech companies, social media platforms, and service providers, making it the industry standard for authorization. The OAuth ecosystem also includes numerous libraries, tools, and frameworks that make integration and implementation easier for developers across various programming languages and platforms.
Authorization for APIs: OAuth 2.0 is widely used for securing APIs, enabling developers to grant fine-grained access control to specific resources while ensuring security and compliance.
What are some best practices for working with OAuth 2.0?
When implementing OAuth 2.0, it’s essential to adhere to the following best practices in order to secure your application and protect user data:

Use short-lived access tokens: Limiting the lifespan of access tokens helps contain the damage if they are compromised. Refresh tokens allow legitimate clients to obtain new access tokens without involving the user.
Limit token scope: Access tokens should always have the smallest scope required for the specific application functionality.
Secure the application against common attack patterns: It is important to take adequate measures to reduce your system’s vulnerability to attack. For instance, using the `state` parameter when initiating an authorization request—and validating the returned state against the initial value—can help protect against CSRF (Cross-Site Request Forgery) attacks. You should also implement rate limiting, which will help prevent Denial-of-Service (DoS) attacks.
Handle access tokens securely: Access tokens should be sent in a request header when the client is requesting a resource from the resource server. They shouldn’t be stored as cookies or transmitted over query parameters. Additionally, the authorization server must include the HTTP “Cache-Control” response header field with a value of “no-store” in any response containing tokens, credentials, or other sensitive information, as well as the “Pragma” response header field with a value of “no-cache”.
Allow users to revoke access to their data: OAuth 2.0 is designed in such a way that the resource owner has complete control of their data. It is therefore important to provide a mechanism to revoke tokens so that users can block unwanted access.
Provide clear documentation: If you’re providing OAuth access to your users’ data, it’s crucial to provide clear, concise, and detailed documentation for the entire OAuth flow. This will help accelerate the onboarding process and increase adoption rates.
What are some challenges of implementing OAuth 2.0?
While OAuth 2.0 offers many benefits, it nevertheless poses several challenges that developers must consider to ensure a successful implementation. These challenges include:

Complexity: OAuth 2.0 is a complex authorization framework that includes many components and interactions. Understanding these components can be challenging, especially for developers who are new to the protocol. For instance, implementing an OAuth 2.0 authorization server involves configuring various endpoints, scopes, and client registrations, which becomes even more complicated when there are multiple clients and different access control requirements.
Secure token management: Token security is essential to a successful OAuth implementation, as improper token management can lead to token leakage or injection attacks. Implementers need to handle token storage, token expiration and revocation, token refreshing, and token usage validation, all of which can be difficult to get right.
User experience: The typical user flow for OAuth 2.0 involves several steps, so it’s important to maintain a smooth and intuitive user experience in order to prevent churn. This can be challenging, especially when it comes to handling errors, designing consent screens, and working across different user agents (i.e., web browsers and mobile apps).
Compatibility and interoperability: OAuth 2.0 has been widely adopted, and there are numerous libraries, frameworks, and implementations available. Still, ensuring compatibility and interoperability between various OAuth 2.0 implementations and providers can be challenging. It’s therefore important to thoroughly test and validate your implementation against different authorization servers and client applications.
How can Postman help you work with OAuth 2.0?
The Postman API Platform includes many features that make it easier for users to work with OAuth 2.0. With Postman, you can:

Leverage built-in support for OAuth: Postman includes built-in support for both OAuth 1.0 and OAuth 2.0, which can be configured at the request, collection, or folder level.
Refresh your OAuth 2.0 access tokens: Postman can automatically refresh OAuth 2.0 access tokens before they expire, which saves the user time by eliminating the need to repeat the entire authorization process.
Quickly authenticate with public APIs: Postman will guide users through the authentication process for several popular APIs, including those that leverage OAuth 2.0. This feature streamlines the authentication process and significantly reduces consumers’ time to first call.
Optionally share tokens with your team: Postman makes it easier to collaborate on OAuth APIs by enabling users to easily share token credentials with other members of their team. Note that Postman won’t share your tokens with your team members unless you specifically tell it to.
https://blog.postman.com/what-is-oauth-2-0/
"""

data = """
The Cave of the Seven Sleepers (Arabic: كهف الرقيم, Kahf ar-Raqīm) is an archaeological and religious site in ar-Rajib, a village to the east of Amman, Jordan.[1] It is claimed that this cave housed the Seven Sleepers, also known from Christian sources as the "Sleepers of Ephesus" and from the Qur’an as the "Companions of the Cave" (Arabic: اصحاب الكهف, romanized: aṣḥāb al kahf)—a group of young men who, according to Byzantine Christian and Islamic sources, fled the religious persecution of Roman emperor Decius.[2][3] Legend has it that these men hid in a cave around AD 250, emerging miraculously centuries later - according to the Quran, 309 lunar years later.[4] Rediscovered in 1951, it is one of several caves associated with the Seven Sleepers (see "Other contenders").

Names and their etymology
Cave of the Seven Sleepers
The English name of this site refers to the seven sleepers who sought refuge in the cave, despite that accounts differ widely concerning the number of sleepers. The canonical Islamic text refers to seven sleeper and a dog.[5]

Kahf ar-Raqīm
The site's Arabic name كهف الرقيم, Kahf ar-Raqīm, is based on the triliteral root ر-ق-م, denoting writing or calligraphy. It may refer to the village or mountain that the cave is located in. It also may refer to the book that recorded the names of the seven sleepers, as is suggested in Muhammad ibn Jarir al-Tabari's exegetical work Tafsir al-Tabari. The nearby village's modern name, al-Rajib, could be a corruption of the term al-raqīm.[5]

Description
The site consists at its core of a rock-hewn ancient burial cave with multiple burials.[6] Some 500 metres west of the cave is a Byzantine cemetery.[6]

The cave is partly natural, partly man-made.[7] The entrance to the cave is flanked by two stone pilasters and two niches, one on each side, vestiges of a Byzantine church.[2] The entrance is from the south, and above it are the remains of a mirab (niche), once part of a mosque.[2] Next to it are traces of a minaret, as well as four Byzantine pillars.[2] An Arabic inscription states that this mosque, the second at the site, was built by orders of the son of Ahmad ibn Tulun, the founder of the Tulunid dynasty (r. 868–884).[2] Archaeologists have concluded that here a Byzantine church was converted into a mosque in the time of Umayyad caliph Abd al-Malik ibn Marwan (d. 705), which underwent renovation under the Tulunids.[2]
"""

p.init()

screen = p.display.set_mode((WIDTH:=800, HEIGHT:=600))
p.display.set_caption("Fast reader")

p.font.init()
font = p.font.SysFont(None, 50)
font_small = p.font.SysFont(None, 30)

words = data.split()
i = 0
pause = False
pause_rendered = False
CONTEXT_LENGTH = 40
JUMP_WORDS = 5
words_per_second = 6.5
while True:
	p.time.wait(int(1000//words_per_second))
	for event in p.event.get():
		if event.type == p.QUIT:
			p.quit()
			quit()
		if event.type == p.KEYDOWN:
			if event.key == p.K_ESCAPE:
				p.quit()
				quit()
			if event.key == p.K_SPACE:
				pause = not pause
				pause_rendered = False
			if event.key == p.K_LEFT:
				i = max(0, i-JUMP_WORDS)
			if event.key == p.K_RIGHT:
				i = min(len(words)-1, i+JUMP_WORDS)
			if event.key == p.K_UP:
				words_per_second += 0.5
			if event.key == p.K_DOWN:
				words_per_second -= 0.5
				words_per_second = max(words_per_second, 0.5)
	if pause and pause_rendered:
		p.time.wait(500)
		continue
	elif pause:
		pause_rendered = True
		screen.fill('black')
		text = font.render(words[i], True, (255, 255, 255))
		text_rect = text.get_rect(center=(800//2, 600//2))
		screen.blit(text, text_rect)

		context_words = words[max(0, i - CONTEXT_LENGTH):i+1]
		context_text = ' '.join(context_words)

		wrapped_lines = []
		line = ''

		for word in context_text.split():
			if font.size(line + word)[0] > 760:  # leave a lil margin from 800
				wrapped_lines.append(line)
				line = word + ' '
			else:
				line += word + ' '
		wrapped_lines.append(line)

		y = 10
		for wrapped_line in wrapped_lines:
			rendered = font.render(wrapped_line.strip(), True, (180, 180, 180))
			screen.blit(rendered, (20, y))
			y += font.get_linesize()
		p.display.flip()
		continue
	
	screen.fill('black')
	# Words per second text
	wps_text = font_small.render("WPS: "+str(words_per_second), True, (0, 255, 0))
	screen.blit(wps_text, (WIDTH-100, HEIGHT-50))
	
    # completed percentage
	completed_percentage = int(i/len(words)*100)
	completed_percentage_text = font_small.render(str(completed_percentage)+"%", True, (0, 255, 0))
	screen.blit(completed_percentage_text, (WIDTH-100, HEIGHT-25))

	text = font_small.render(words[i], True, (255, 255, 255))
	text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
	screen.blit(text, text_rect)
	p.display.flip()
	i += 1
	if i == len(words):
		end_text = font.render("THE END", True, (0, 255, 0))
		screen.blit(end_text, (WIDTH//2, HEIGHT//2))
		p.display.flip()
		p.time.wait(1000)
		p.quit()
		quit()