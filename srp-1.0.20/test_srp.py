import srp

# Consider enabling RFC5054 compatibility for interoperation with non pysrp SRP-6a implementations
#srp.rfc5054_enable()

# The salt and verifier returned from srp.create_salted_verification_key() should be
# stored on the server.

#file io for 'server'
def tester(client,server):
    with open("client files/test"+ str(client) +".py","r") as f:
        string = f.read()
    print(string)
        
    salt, vkey = srp.create_salted_verification_key( 'mouse', string )

    class AuthenticationFailed (Exception):
        pass

    # ~~~ Begin Authentication ~~~

    #file io for 'client'
    with open("server files/test copy"+ str(server) +".py","r") as f:
        string2 = f.read()
    print(string2)

    usr      = srp.User( 'mouse', string2 )
    uname, A = usr.start_authentication()


    # The authentication process can fail at each step from this
    # point on. To comply with the SRP protocol, the authentication
    # process should be aborted on the first failure.

    # Client => Server: username, A
    svr      = srp.Verifier( uname, salt, vkey, A )
    s,B      = svr.get_challenge()


    if s is None or B is None:
        raise AuthenticationFailed()

    # Server => Client: s, B
    M        = usr.process_challenge( s, B )


    if M is None:
        raise AuthenticationFailed()

    # Client => Server: M
    HAMK     = svr.verify_session( M )


    if HAMK is None:
        raise AuthenticationFailed()

    # Server => Client: HAMK
    usr.verify_session( HAMK )

    # At this point the authentication process is complete.

    # print(usr.authenticated())
    # print(svr.authenticated())
    if (usr.authenticated() and svr.authenticated()):
        print('YOU HAVE THE SAME FILE AS OTHER USER! AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH')
        return
    print("FILES WERE DIFFERENT :)")

    # assert usr.authenticated()
    # assert svr.authenticated()

    

tester(1,1)