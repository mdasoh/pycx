import signal, os, sys, fcntl, select, socket
from pycx import cx, atom

top = atom( None, 1 )
top.context.ins( atom( top, 1 ) )
#print( top.tocx() )
top.context.first.clothe()
top.context.dub( 'us' )
top.context.first.context.dub( 'utah' )

topq = None

class queue:
    def __init__( self, sock, load ):
        global topq
        self.next = None
        self.text = load
        self.sock = sock
        if not topq:
            topq = self
        else:
            here = topq
            while here.next:
                here = here.next
            here.next = self


flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
flags |= os.O_NONBLOCK | os.O_ASYNC
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, flags)
fcntl.fcntl(sys.stdin, fcntl.F_SETOWN, os.getpid())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind(('localhost', 5001))
server.listen(5) #backlog of five connections

flags_s = fcntl.fcntl(server, fcntl.F_GETFL)
flags_s |= os.O_NONBLOCK | os.O_ASYNC
fcntl.fcntl(server, fcntl.F_SETFL, flags_s)
fcntl.fcntl(server, fcntl.F_SETOWN, os.getpid())

in1 = []
in2 = [ sys.stdin, server ]
ou2 = []

exiting = 0

global mode, cplt, cx

mode = 0
#reset to 0 after each write.
cplt = 0
cx = ''

qu1 = []

def io_( signum, frame ):
    global exiting
    #print( 'Signal handler called with signal', signum )
    #recv_data = ''
    while in2:
        in3 = []
        for i in in2:
            #if int( i ) < 0:	# nwhat was -1 in an error message?
            #    continue
            in3.append( i )
        for i in in1:
            #if i < 0:
            #    continue
            in3.append( i )
        rd1, wr1, xc1 = select.select( in3, ou2, in2, 0 )
        if not rd1:
            del in3
            break
        for s in rd1:
            if s is sys.stdin:
                print( 'read' )
                read_data = s.read( 1 )
            if s is server:
                print( 'serv' )
                conn = None
                conn_addr = None
                try:
                    conn, conn_addr = s.accept()
                except:
                    continue
                in1.append( conn )
                flags_c = fcntl.fcntl(conn, fcntl.F_GETFL)
                flags_c |= os.O_NONBLOCK | os.O_ASYNC
                fcntl.fcntl(conn, fcntl.F_SETFL, flags_c)
                fcntl.fcntl(conn, fcntl.F_SETOWN, os.getpid())
                #continue
            for i in in1:
                if s is i:
                    try:
                        recv_data = s.recv( 4096 )
                    except:
                        continue
                    if not recv_data:
                        in1.remove( s )
                        s.close()
                    else:
                        ##if cplt == 2:
                        ##queue( s, str( cplt ) )
                        queue( s, recv_data )
                    #print( str( recv_data ) )	# so long...
                    #print( 'nput' )

########



########

fi1 = open( '0004' )
for line in fi1:
    #print( line, ' x' )
    for s in line.splitlines():
        line = line.rstrip( '\r\n' )
        queue( sys.stdout, ( s + '\r\n' ).encode( 'utf-8' ) )
fi1.close()

signal.signal( signal.SIGALRM, io_ )
signal.setitimer( signal.ITIMER_REAL, 0.1 ) #, 1

signal.signal( signal.SIGIO, io_ )

def wfun( lev0, fi ):
    if lev0:
        print( 'considering: ', lev0.tocx() )
        bah = lev0.context.elems()
    else:
        return
    it = 0
    if( bah == 0 ):
        bah = 1
    while it < bah:
        while( lev0 ):
            print( 'saving: ', lev0.tocx() )
            fi.write( 'put\r\n' )
            fi.write( lev0.tocx() )
            fi.write( '\r\n' )
            if lev0.id_mask == 2:
                fi.write( lev0.text.decode( 'utf-8' ).rstrip( '\r\n' ) )
            fi.write( '\r\n' )
            if lev0.context:
                if lev0.context.first:
                    wfun( lev0.context.first, fi )
                lev0 = lev0.context.next
            else:
                break
        it = it + 1
    #else:
    #    fi.write( 'put\r\n' )
    #    fi.write( lev0.tocx() )
    #    fi.write( '\r\n' )
    #    if lev0.id_mask == 2:
    #        fi.write( lev0.text )
    #    fi.write( '\r\n' )

while not exiting:
    signal.pause()
    recv_data = None
    while topq:
        print( 'recv_data: ', topq.text )
        recv_data = topq.text.decode( 'utf-8' )
        print( 'recv_data_: ', recv_data )
        for recvd in recv_data.splitlines( True ): # preserve newlines
            ##if recv_data and 0:
            recv_d = recvd
            #.encode( 'utf-8' )
            print( "recv_d: ", recv_d )
            if recv_d == 'get\r\n' or recv_d == 'get\n':
                print( "mode 0\n" )
                mode = 0
                cplt = 0
                del cx
                cx = ''
            elif recv_d == 'mget\r\n' or recv_d == 'mget\n': # note: elif/else
                mode = 4
                cplt = 0
                del cx
                cx = ''
            elif ( recv_d == 'put\r\n' or recv_d == 'put\n' ) and cplt != 2:
                #print( 'put !!' )
                mode = 1
                cplt = 0
                del cx
                cx = ''
            elif recv_d == 'link\r\n' or recv_d == 'link\n':
                print( 'link method' )
                mode = 2
                cplt = 0
                del cx
                cx = ''
            elif recv_d == 'say\r\n' or recv_d == 'say\n':
                fi2 = open( '0004', 'w' )
                lev0 = top
                wfun( lev0, fi2 )
                #fi2.write( '@echo off\n' )
                #fi2.write( 'cls\n' )
                fi2.close()
            elif recv_d == 'exit\r\n' or recv_d == 'exit\n':
                mode = 0
                cplt = 0
                in1.remove( topq.sock )
                if topq.sock:
                    topq.sock.close()
                topq = topq.next
                break
                #continue
            elif recv_d == 'hup\r\n' or recv_d == 'hup\n':
                print( 'hup !!' )
                exiting = 1 # cannot say = 1 because then, variable is local # solved, global.
            else:
                #for st in recv_data.splitlines():
                s = str( recvd ).rstrip( '\r\n' )
                #s = st.encode( 'utf-8' )
                #print( s, 'n' ) # mebby a useful debug measure
                print( "cplt: ", cplt )
                #if ( cplt == 0 ) or ( not s.encode( 'utf-8' ).startswith( b'.'.decode( 'utf-8' ) ):
                #if ( cplt == 0 ) or ( not s.startswith( b'.'.decode( 'utf-8' ) ) ):
                if ( cplt == 0 ) or ( cplt < 2 and s.startswith( '.' ) ):
                    if not s.startswith( '.' ):
                        #print( 'here' )
                        cplt = 1
                    if cx:
                        #cx = '.'.join([ s.decode( 'utf-8' ).strip( '.' ), cx ])
                        cx = '.'.join([ s.strip( '.' ), cx ])
                    else:
                        #cx = s.decode( 'utf-8' ).strip( '.' )
                        cx = s.strip( '.' )
                    if not s.startswith( '.' ):
                        #cplt = 2
                        print( 'cplt0: ', s )
                        cplt = 1
                elif cplt == 1:
                    #cx = '.'.join([ s.decode( 'utf-8' ).strip( '.' ), cx ])
                    #cplt = 2 # move along.
                    #elif cplt == 2:
                    #queue( s, recv_data )
                    print( "xcx: ", cx )
                    cplt = 2
                #if cplt != 1: # 2:
                #    continue
                if cplt == 2:
                    multiple = 0
                    cx_ = cx
                    cx_b = cx
                    if( cx.endswith( '.us' ) ):
                        cx_a = cx.split( '.' )[ 1 ]
                    else:
                        cx_a = 'us'
                    while mode == 0 or mode == 4:
                        cx = cx_
                        #jun topq.sock.send( b'initial: ' + cx.encode( 'utf-8' ) + b'\n' )
                        #topq.sock.send( b'prove: ' + top.context.first.context.first.context.name.encode( 'utf-8' ) + b'\n' )
                        #topq.sock.send( b'prove: ' + top.context.first.context.first.context.next.context.name.encode( 'utf-8' ) + b'\n' )
                        #topq.sock.send( cx.encode( 'utf-8' ) )
                        #topq.sock.send( b'\n' )
                        if cx.endswith( '.us' ):
                            #jun topq.sock.send( b'getting: ' )
                            #jun topq.sock.send( cx.encode( 'utf-8' ) )
                            #jun topq.sock.send( b'\n' )
                            #jun topq.sock.send( topq.text )
                            cxs = cx.split( '.' )
                            it = len( cxs ) - 2 # skip .us
                            cxh = top
                            while it > -1:
                                #jun topq.sock.send( str( it ).encode( 'utf-8' ) + b' ' )
                                #jun topq.sock.send( cxs[ it ].encode( 'utf-8' ) + b'\n' )
                                #0 topq.sock.send( cxt.tocx().encode( 'utf-8' ) + b'\n' )
                                #jun topq.sock.send( b'\n' )
                                cxt = cxh
                                #topq.sock.send( b'top' )
                                if cxh.context and cxh.context.has( cxs[ it ] ): # has forms a linked circle
                                    #jun topq.sock.send( b'o' + str( it ).encode( 'utf-8' ) )
                                    print( 'has: ', cxh.context.has( cxs[ it ] ) )
                                    #cxf = cxh.context.which( cxs[ it ] )
                                    cxt = cxh.cxtoptr( cxs[ it ] )
                                    if( it == 0 ): # and cx == cx_:
                                        if cxh.context and cxh.context.has( cx_.split( '.' )[ it ] ): # has forms a linked circle
                                            #topq.sock.send( b'cx_: ' + cx_.split( '.' )[ it ].encode( 'utf-8' ) + b'\n' )
                                            cx_ = cx_.split( '.' )[ it ] + '.' + cxh.tocx()
                                            #topq.sock.send( b'found: ' + cxh.tocx().encode( 'utf-8' ) + b'\n' )
                                            #topq.sock.send( b'found: ' + cxt.tocx().encode( 'utf-8' ) + b'\n' )
                                        print( cxt.tocx() ) # us.us
                                        topq.sock.send( cxt.tocx().encode( 'utf-8' ) + b'\n' ) # us.us
                                        #jun topq.sock.send( b'\n' )
                                        if cxt.id_mask == 2:
                                            print( 'line text: ', cxt.text )
                                            topq.sock.send( cxt.text ) # us.us
                                        else:
                                            topq.sock.send( b'\n' ) # us.us
                                        if mode == 0:
                                            break
                                        #topq.sock.send( b'a\n' )
                                        print( 'cxt0: ', cxt.context.name, 'last: ', cxt.context.prev, 'next: ', cxt.context.next )
                                        if cxt.context.prev:
                                            print( 'prev: ', cxt.context.prev.context.name )
                                        #topq.sock.send( b'b\n' )
                                        #topq.sock.send( b'prove: ' + top.context.first.context.first.context.name.encode( 'utf-8' ) + b'\n' )
                                        #topq.sock.send( b'prove: ' + top.context.first.context.first.context.next.context.name.encode( 'utf-8' ) + b'\n' )
                                        if cxt.context.first and cxt.context.first.context:
                                            #topq.sock.send( b'd\n' )
                                            #jun topq.sock.send( b'first: ' + cxt.context.first.context.name.encode( 'utf-8' ) + b'\n' )
                                            #topq.sock.send( b'e\n' )
                                            if cxt.context.first.context.name:
                                                #jun? cx_ = cxt.context.next.context.name + '.' + cxh.tocx()
                                                cx_ = cxt.context.first.context.name + '.' + cxt.tocx()
                                                cxs = cx_.split( '.' )
                                                it = len( cxs ) - 2 # skip .us
                                                cxh = top
                                                continue
                                            else:
                                                #topq.sock.send( b'missed 0001\n' )
                                                #topq.sock.send( cxt.tocx().encode( 'utf-8' ) + b'\n' )
                                                cx_ = '0' + '.' + cxt.tocx()
                                                cxs = cx_.split( '.' )
                                                it = len( cxs ) - 2 # skip .us
                                                cxh = top
                                                continue
                                            #jun topq.sock.send( b'within: ' + cxt.tocx().encode( 'utf-8' ) + b'\n' )
                                            #cx = cx_
                                            #it = it + 1 # terra terra.utah.us
                                            #it = it - 1 # sunset utah.us
                                        elif cxt.context.first:
                                            #topq.sock.send( b'missed 0002\n' )
                                            #jun more code due here...
                                            continue # heretofore unencountered.
                                        elif cxt.context.next:
                                            if cxh.tocx() == cx_b.split( '.', 1 )[ 1 ]:
                                                mode = 0
                                                break
                                            if cxt.context.next.context and cxt.context.next.context.name:
                                                cx_ = cxt.context.next.context.name + '.' + cxh.tocx()
                                                #topq.sock.send( b'missed 0003\n' )
                                            else:
                                                multiple = multiple + 1
                                                sis = str( multiple ).encode( 'utf-8' ) + b'.'
                                                #topq.sock.send( b'missed 0004: ' + sis + b'\n' )
                                                cx_ = str( multiple ) + '.' + cxh.tocx()
                                            #print( 'next: ', cxt.context.next.context.name )
                                            #jun topq.sock.send( b'next: ' + cxt.context.next.context.name.encode( 'utf-8' ) + b'\n' )
                                        else:
                                            #topq.sock.send( b'vital: ' + cxt.tocx().encode( 'utf-8' ) + b'\n' )
                                            #topq.sock.send( b'p_next: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                            #if cxt.tocx() == cx_b:
                                            #topq.sock.send( b'overtailed 0001 ' + cxh.tocx().encode( 'utf-8' ) + b'\n' )
                                            #topq.sock.send( b'overtailed 0001 ' + cxh.tocx().split( '.', 1 )[ 1 ].encode( 'utf-8' ) + b'\n' )
                                            #topq.sock.send( b'overtailed 0001 ' + cx_b.split( '.', 1 )[ 1 ].encode( 'utf-8' ) + b'\n' )
                                            if cxh.tocx() == cx_b.split( '.', 1 )[ 1 ]:
                                                mode = 0
                                                break
                                            if cxt.tocx().split( '.', 1 )[ 1 ] == cx_b:
                                                mode = 0
                                                break
                                            cxt = cxt.parent
                                            #it = it + 1
                                            #if not cxt.parent:
                                            #    break
                                            while cxt.parent:
                                                #topq.sock.send( b'prove: ' + top.context.first.context.first.context.name.encode( 'utf-8' ) + b'\n' )
                                                #topq.sock.send( b'prove: ' + top.context.first.context.first.context.next.context.name.encode( 'utf-8' ) + b'\n' )
                                                #if( cxt == top.context.first.context.first ):
                                                #    #topq.sock.send( b'equal: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                                #    print( 'equal: ', cxt.context.next.context, '\n' )
                                                if cxt.tocx().split( '.', 1 )[ 1 ] == cx_b:
                                                    mode = 0
                                                    break
                                                #if cxt.tocx() == cx_b:
                                                #    topq.sock.send( b'overtailed 0002\n' )
                                                #topq.sock.send( cxt.tocx().encode( 'utf-8' ) + b' ' + cx_b.encode( 'utf-8' ) )
                                                cxt = cxt.parent
                                                it == it + 1 # unused
                                                #topq.sock.send( b'p_rent: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                                #topq.sock.send( b'prove: ' + top.context.first.context.first.context.name.encode( 'utf-8' ) + b'\n' )
                                                #topq.sock.send( b'prove: ' + top.context.first.context.first.context.next.context.name.encode( 'utf-8' ) + b'\n' )
                                                if not cxt.context.next: # is None:
                                                    continue
                                                else:
                                                    break
                                            if not cxt.parent:
                                                #topq.sock.send( b'nak\n' )
                                                break
                                            #topq.sock.send( b'p_next: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                            if not cxt.context.next:
                                                #topq.sock.send( b'name: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                                break
                                            #topq.sock.send( b'p_next: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                            cxt = cxt.context.next
                                            #topq.sock.send( b'p_next: ' + cxt.context.name.encode( 'utf-8' ) + b'\n' )
                                            #topq.sock.send( b'p_tocx: ' + cxt.tocx().encode( 'utf-8' ) + b'\n' )
                                            #if not cxt:
                                            #    break
                                            #cxt = cxt.parent
                                            cx_ = cxt.tocx()
                                            #it = it + 1
                                            it = 0
                                            cxs = cx_.split( '.' )
                                            #it = len( cxs ) - 2 # skip .us
                                            cxh = cxt.parent
                                            #cx = cx_
                                            continue
                                        #topq.sock.send( b'\n' )
                                    #else:
                                    #    topq.sock.send( b'it != 0\n' )
                                else:
                                    topq.sock.send( b'not related: ' )
                                    topq.sock.send( cxs[ it ].encode( 'utf-8' ) )
                                    topq.sock.send( b' ' )
                                    topq.sock.send( cxh.tocx().encode( 'utf-8' ) )
                                    topq.sock.send( b'\n' )
                                    break
                                cxh = cxt
                                #topq.sock.send( cxh.cxtoptr( cxs[ it ] ).tocx().encode( 'utf-8' ) )
                                #topq.sock.send( top.cxtoptr( 'd.c.b.0.one' ).tocx().encode( 'utf-8' ) )
                                #topq.sock.send( top.context.first.cxtoptr( 'd.c.b.0.one' ).tocx().encode( 'utf-8' ) )
                                it = it - 1
                        else:
                            print( b'not ends with .us: ' + cx.encode( 'utf-8' ) )
                            topq.sock.send( b'error in context as specified 0001\n' )
                        if mode == 0:
                            #topq.sock.send( b'break 0\n' )
                            break
                        elif cx_a == cx_:
                            #topq.sock.send( b'break 1\n' )
                            break
                        else:
                            #jun topq.sock.send( b'cx: ' + cx.encode( 'utf_8' ) + b'\n' )
                            cx_a = cx_
                            #cx = 'orem.utah.us';
                        #topq.sock.send( b"....\n" );
                        print( 'got: ', cx )
                    ##print( ': ', recv_data )
                    ##if( mode == 0 ) and 0:
                    #send
                    #print( 'getting: ', cx )
                    #topq.sock.send( topq.text.encode( 'utf-8' ) )
                    #topq.sock.send( b'\n' )
                    #if( cplt == 2 ):
                    #    print( 'got' )
                    if mode == 1:
                        print( 'put method called' )
                        if cx.endswith( '.us' ):
                            if topq.sock != sys.stdout:
                                topq.sock.send( b'putting: ' )
                                topq.sock.send( cx.encode( 'utf-8' ) )
                                topq.sock.send( b'\n' )
                            #topq.sock.send( topq.text )
                            cxs = cx.split( '.' )
                            it = len( cxs ) - 2 # skip .us
                            cxh = top
                            while it > -1:
                                #topq.sock.send( cxs[ it ].encode( 'utf-8' ) )
                                #topq.sock.send( b'\n' )
                                cxt = cxh
                                if cxh.context:
                                    print( 'here' )
                                    leh = 0
                                    #cxf = cxh.context.which( cxs[ it ] )
                                    if cxh.context.has( cxs[ it ] ):
                                        #print( 'cxh: ', cxh.tocx() )
                                        #print( 'cxt: ', cxt.tocx() )
                                        leh = 1
                                    cxt = cxh.cxtoptr( cxs[ it ] )
                                    if not leh:
                                        print( 'cxh: ', cxh.tocx() )
                                        print( 'cxt: ', cxt.tocx() )
                                        cxt = cxt.lineup()
                                        print( 'cxh: ', cxh.tocx() )
                                        print( 'cxt: ', cxt.tocx() )
                                        #del cxt.text
                                        print( '*** creating line ***' )
                                        cxt.text = topq.text
                                    if( it == 0 ):
                                        if topq.sock != sys.stdout:
                                            topq.sock.send( cxt.tocx().encode( 'utf-8' ) )
                                            topq.sock.send( b'\n' )
                                            topq.sock.send( topq.text )
                                            #topq.sock.send( b'\n' )
                                    print( 'not exiting' )
                                else:
                                    if topq.sock != sys.stdout:
                                        topq.sock.send( b'not related: ' )
                                        topq.sock.send( cxs[ it ].encode( 'utf-8' ) )
                                        topq.sock.send( b' ' )
                                        topq.sock.send( cxh.tocx().encode( 'utf-8' ) )
                                        topq.sock.send( b'\n' )
                                    break
                                cxh = cxt
                                #topq.sock.send( cxh.cxtoptr( cxs[ it ] ).tocx().encode( 'utf-8' ) )
                                #topq.sock.send( top.cxtoptr( 'd.c.b.0.one' ).tocx().encode( 'utf-8' ) )
                                #topq.sock.send( top.context.first.cxtoptr( 'd.c.b.0.one' ).tocx().encode( 'utf-8' ) )
                                it = it - 1
                        else:
                            if topq.sock != sys.stdout:
                                topq.sock.send( b'error in context as specified 0002\n' )
                        print( 'putting: ', cx )
                        mode = 0
                    elif mode == 2:
                        if not cx.endswith( '.us' ):
                            if topq.sock != sys.stdout:
                                topq.sock.send( b'error in context as specified 0003\n' )
                        lx = topq.text.decode( 'utf-8' ).rstrip( '\r\n' )
                        #lx = lx.rstrip( '\r' )
                        print( 'linking: ', lx )
                        if not lx.endswith( '.us' ):
                            if topq.sock != sys.stdout:
                                topq.sock.send( b'error in link as specified 0004\n' )
                        else:
                            cxs = cx.split( '.' )
                            lxs = lx.split( '.' )
                            it = len( cxs ) - 2 # skip .us
                            itl = len( lxs ) - 2
                            cxh = top
                            lxh = top
                            lxt = None
                            while itl > -1:
                                #lxt = lxh
                                if not lxh.context:
                                    break
                                if not lxh.context.has( lxs[ itl ] ):
                                    print( 'link not found' )
                                    break
                                lxt = lxh.cxtoptr( lxs[ itl ] )
                                lxh = lxt
                                itl = itl - 1
                            while it > -1 and lxt:
                                ##### begin paste
                                cxt = cxh
                                if cxh.context:
                                    leh = 0
                                    if cxh.context.has( cxs[ it ] ):
                                        leh = 1
                                    #cxt = cxh.cxtoptr( cxs[ it ] )
                                    cxt = cxh.cxtoptr( cxs[ it ] )
                                    if not leh:
                                        cxt = cxt.linkup()
                                        bit = 0
                                        while bit < cxh.context.elems():
                                            print( bit, cxh.context.which( cxt ) )
                                            bit = bit + 1
                                        cxt.point( lxt )
                                        print( 'cxh: ', cxh.tocx(), cxh.id_mask )
                                        print( 'cxt: ', cxt.tocx(), cxt.id_mask )
                                        #cxt = cxt.linkup()
                                        #if cxt.to:
                                        #    del cxt.to
                                        #cxt.to = lxt
                                    if( it == 0 ):
                                        if topq.sock != sys.stdout:
                                            topq.sock.send( cxt.tocx().encode( 'utf-8' ) )
                                            topq.sock.send( b' -> ' )
                                            topq.sock.send( lx.encode( 'utf-8' ) )
                                            topq.sock.send( b'\n' )
                                else:
                                    if topq.sock != sys.stdout:
                                        topq.sock.send( b'not related: ' )
                                        topq.sock.send( cxs[ it ].encode( 'utf-8' ) )
                                        topq.sock.send( b' ' )
                                        topq.sock.send( cxh.tocx().encode( 'utf-8' ) )
                                        topq.sock.send( b'\n' )
                                    break
                                cxh = cxt
                                it = it - 1
                                ##### end paste
                        mode = 0
                    del cx
                    cx = '' # get is the defaults, may happen next time around
                    cplt = 0 # was 2, we work a line at a time.
        temp = topq
        if topq:
            topq = topq.next
        del temp

print( 'exit' )

for i in in1:
    in1.remove( i )
    i.close()
server.close()

#top.context.first.context.ins( atom( top.context.first, 1 ) )
#top.context.first.context.first.clothe()
#top.context.first.context.first.context.ins( atom( top.context.first.context.first, 1 ) )
#top.context.first.context.first.context.first.clothe()
#top.context.first.context.first.context.first.context.ins( atom( top.context.first.context.first.context.first, 1 ) )
#top.context.first.context.first.context.dub( 'one' )
#top.context.dub( 'name' )
#print( top.context.first.context.first.context.first.context.first.tocx() )
#print( top.tocx() )
#print( top.context.first.tocx() )
#print( top.context.first.context.first.tocx() )
#print( top.context.first.context.first.context.first.tocx() )
#top.context.first.context.first.context.first.cxtoptr( 'd.c.b.0' )
#top.context.first.cxtoptr( 'd.c.b.0.one' )
#top.context.first.context.first.cxtoptr( 'd.c.b.0.one' )
#top.context.first.context.first.cxtoptr( 'c.b.0.one.0' )
#print( top.context.first.context.first.context.first.context.first.tocx() )
