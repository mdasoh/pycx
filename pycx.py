#!/usr/bin/python3

class cx:
    def __init__(self, a):
        self.a = a
        self.name = None
        self.up = None
        if a.parent:
            if not a.parent.context:
                a.parent.clothe()
            self.up = a.parent.context
        self.prev = None
        self.next = None
        self.first = None
        self.last = None
    def dele(self, node):
        it = self.first
        if it == node:
            if it == self.last:
                self.last = self.first = None
            else:
                self.first = it.context.next
            if it.context:
                del it.context
            del node
            return self
        while it:			# != None
            if it.context.next == node:
                it.context.next = node.context.next
                if it.context.next != None:
                    it.context.next.context.prev = it
                if node == self.last:
                    self.last = node.context.prev
                del node
                break
            it = it.context.next
        return self
        return None
    def isol(self, a):
        it = self.first
        if it == a:
            if it == self.last:
                self.last = self.first = None
            #else: # new
            if it.context:
                self.first = it.context.next
                if a.context.prev:
                    print( '*alert*' )
                    a.context.prev = None
                a.context.next = None
            return a
        while it:
            if it.context.next == a:
                #if a.context.prev:
                #    a.context.prev.next = a.context.next
                it.context.next = a.context.next
                if it.context.next:
                    it.context.next.context.prev = it
                if a == self.last:
                    self.last = a.context.prev
                a.context.prev = a.context.next = None
                return a
            it = it.context.next
        return None
    def ins(self, no):			# appends to the end
        no.parent = self.a
        if no.context:
            no.context.up = self
        if not self.first:		# first
            self.last = self.first = no
        #elif self.last == self.first and not self.context:	# taken care of elsewhere, or else could not be called
        #    #self.first = no		# this could be the best fix of aug 2018
        #    self.a.clothe()		# so this makes no sense.  excluded.  again.
        else:
            if not no.context:		# this inserts last.
                no.context = cx( no )
                no.context.up = self
            no.context.prev = self.last
            if not self.last.context:
                self.last.context = cx( self.last )
            self.last.context.next = no
            self.last = no		# .prev (bug), fixed.
            #no.next == None
            print( 'inserting: ', no.context.prev.context.name, ' and: ', no.context.name, ' at: ', self.name )
        return no
    def ins_by(self, ne, no):		# above ne
        no.parent = self.a
        if no.context:
            no.context.up = self
        if not ne.context:
            ne.context = cx( ne )
            self.first = ne
        it = self.first
        while it:
            if it == ne:
                if not no.context:
                    no.context = cx( no )
                no.context.prev = ne
                no.context.next = ne.context.next
                ne.context.next = no
                if self.last == ne:	# last
                    self.last = no
            it = it.context.next
        return no
    def ins_at(self, ne, no):		# before ne
        if not ne:
            print( '*alert*' )
            return None
        no.parent = self.a
        if not self.first:		# new
            self.first = self.last = ne	# hijack empty context, calling with nonincluded
        if no.context:
            no.context.up = self
        if not ne.context:
            printf( "ins ncx" )
            ne.context = cx( ne )
            ne.context.up = self	# fixx
            self.last = ne
        it = self.first
        if self.first == ne:		# first
            print( 'inserting first' )
            self.first = no
        bah = 0
        while it and bah < 5:
            if it == ne:
                print( 'inserting at' )
                if not no.context:
                    no.context = cx( no )
                    no.context.up = self # and what's going on here?
                if ne.context.prev:	# new
                    print( ne.context.prev.context.name )
                    print( 'updating prev: ', ne.context.name )
                    ne.context.prev.context.next = no
                no.context.prev = ne.context.prev
                no.context.next = ne
                ne.context.prev = no
                #if not self.first:
                #    print( 'return 0' )
                #if no == self.first:
                #    print( 'return 0' )
                #faz = self.first
                #pit = 0				# new
                #while faz:
                #    #if faz == no.context.
                #    if pit == 5:
                #        break
                #    if faz.context.name:
                #        print( 'there: ', faz.context.name )
                #    else:
                #        print( 'there enumerated' )
                #    #if faz.context.next == no:
                #    if faz == no:
                #        print( 'return it' )	# ???
                #    pit += 1
                #    faz = faz.context.next
                #print( 'searched ', pit )
                ##return None
            bah = bah + 1	# thanks
            it = it.context.next
        print( "ins_at: ne.context ", ne.context.name, ' no.context ', no.context.name )
        print( "ins_at: elem ", self.elem( no ) )
        return no
    def index(self, seq):
        if not self.first:
            return None
        it = 0
        here = self.first
        while it < seq:
            if not here:		# as the following:
                break
            if here.context:		# None has no context.  line 188?
                here = here.context.next
            else:
                break
            it += 1
        return here
    def elems(self):
        if not self.first:
            return 0
        it = 1				# was 0.  important fix, aug 2018
        here = self.first
        if not here.context:
            return 1			# not a constraint.
        while here: #and it < 20:
            here = here.context.next
            if( here ):
                print( "first: ", here.context )
            #print( str( here ), ':', str( it ) )
            if( it > 80 ):
                print( 'too many' )
                return 0
            if( self.up and here == self.up.last ):
                break
            it += 1
        return it
    def elem(self, node):		# enumerate
        if not self.first:
            return 0
        if node == self.first:
            return 0
        here = self.first.context.next
        it = 1 #0				# new
        while here:
            if here.context.name:
                print( 'here: ', here.context.name )
            else:
                print( 'here enumerated' )
            #if here.context.next == node:
            if here == node:
                return it
            it += 1
            here = here.context.next
        return None
    def which(self, node):		# compare elem()
        if not self.first:
            print( 'not on first' )
            return None
        if node == self.first:
            if node.context and node.context.name:
                return node.context.name
            return '0'
        here = self.first.context.next
        it = 1				# new 0, reverted
        while here:
            if here == node: #.context.next == node:
                if node.context.name:
                    print( 'ncn: ', node.context.name )
                    return node.context.name
                return str( it )
            it += 1
            here = here.context.next
        print( 'wch' )
        return None
    def has(self, node):
        if not self.first:
            return None
        #if node == self.name:
        #    return self.name
        if not node:
            return None
        here = self.first
        it = 0 # 1  (# -1)
        itc = self.elems() # 2
        print( 'elems: ', itc )
        #if( self.first.context.next ):	# last of several important fixes.  also: again, above.
        #    print( 'next: ', self.first.context.next.context.name )
        if( self.last.context ):
            print( 'last: ', self.last.context.name )
        while here:
            if not here:
                break
            print( 'here.context', here.context )
            if here.context and here.context.name:
                print( 'here.context.name', here.context.name )
                print( here.context.name, ' ', node, 'x', str( it ) ) # next -> here.
                print( 'node: ', node, 'name: ', here.context.name )
                if node == here.context.name:
                    return here.context.name
            idx = None
            if node.isdigit():
                ## it = 0
                #here = self.first
                idx = None
                if self.first:
                    idx = here #self.index( int( node ) )
            if idx:
                print( 'tocx: x', str( self.elem( idx ) ), 'y node: x', node, 'y' )
                if str( self.elem( idx ) ) == node:
                    print( 'verified' )
                if not here:
                    return None
                #elif here.context and here.context.first and node == self.elem( self.index( int( node ) ) ): # index() #if
                elif node == str( self.elem( idx ) ): # index() #if
                    if here.context and here.context.name:
                        print( 'not returning name: ', here.context.name )
                        return None # here.context.name
                    print( 'returning num: ', str( self.elem( idx ) ) )
                    return str( self.elem( idx ) )
            it = it + 1
            if here != self.last: # ???
                print( 'no name?', here.context.next, here.context.name, it )
            if it < 0: # -1 -1 -1 -1 -1 looks like a fix, was ==
                return None
            if here == self.last: # thank you fix
                return None
            here = here.context.next # thank you fix
        return here
        print( 'has' )
        return None
    def dub(self, string):
        print( 'dubbing' )
        if string == 'None':
            print( '*alert*' )
        elif string == None:
            print( '*alert*' )
        elif string.isdigit():		# if an integer, reorder accordingly
            if not self.up:
                print( 'no up' )
                return None
            boom = self.up
            sir = int( string )  
            print( 'counting' )
            print( 'a0: ', boom.up.first )
            if( boom.up.first.context ):
                print( 'a1: ', boom.up.first.context.next )
                if( boom.up.first.context.next ):
                    print( 'a2: ', boom.up.first.context.next.context.next )
            #print( 'a3: ', boom.up.first.context.next.context.next.context.next )
            #print( 'a4: ', boom.up.first.context.next.context.next.context.next.context.next )
            #print( 'a5: ', boom.up.first.context.next.context.next.context.next.context.next.context.next )
            if sir > boom.elems() - 1:
                print( 'out of range' )
                return None
            print( 'isolating' )
            sis = boom.isol( self.a )
            print( 'indexing 1' )
            if sir == boom.elems():
                bah = boom.index( sir - 1 )
                boom.ins_by( bah, sis )
                return self
            print( 'indexing 2' )
            bah = boom.index( sir )
            print( 'dubbah1: ', boom.elem( bah ) ) # 1
            boom.ins_at( bah, sis )
            print( 'dubbah3: ', boom.elem( sis ) )
            print( 'dubbah2: ', boom.elem( bah ) )
            return self
        else:
            self.name = string
        return self
#

class atom:
    def __init__(self, p, id):
        self.parent = p
        self.id_mask = id
        if p == None:
            self.context = cx( self )
        else:
            self.context = None
        #if c:
        #    self.clothe()
        #    self.context.name = c
    def clothe(self):			# implement recursively
        if self.context:
            return self.context
        self.context = cx( self )	# seemed to expose a flaw in cx::ins(), fixed.
        return self.context
    def cxtoptr(self, place):
        if place.endswith( '.' ):
            return None
        if place.endswith( ';' ):
            return None
        if place.count( '{' ):
            return None
        if place.count( '{' ):
            return None
        if place.count( ' ' ):
            return None
        if place.count( '\r' ):
            return None
        if place.count( '\n' ):
            return None
        sis = self.tocx()
        while place.startswith( '.' ):	# relative contexts start with .
            sis = sis[ sis.find( '.' ) + 1 : len( sis ) ]
            place = place[ 1 : len( place ) ]
        bah = place.split( '.' )	# cx of referent as additive
        boom = sis.split( '.' )		# cx of referent as relative
        print( 'ctp0: bah ', str( bah ), ' boom ', str( boom ) )
        bar = None
        faz = None			# parent
        if place.count( '.' ):		# search
            it = 0
            while it < len( boom ):
                #print( 'ctp1: bah ', str( bah ), ' boom ', str( boom ) )
                #print( ' bar ', str( bar ), ' faz ', str( faz ) )
                #print( ' it ', str( it ), ' ta ', str( ta ) )
                #print( ' sis ', sis, ' itc ', str( itc ) )
                ta = 0
                itc = 0
                while ta < len( bah ):
                    if( len( boom ) - 1 - it == -1 ):
                        break
                    if boom[ len( boom ) - 1 - it ] == bah[ len( bah ) - 1 - ta ]:
                        ta = ta + 1
                        it = it + 1
                    else:
                        if ta > 0:
                            ta = -1
                        else:
                            itc = 1
                        break
                if ta == -1:		#
                    break
                if it == len( boom ) and self.context: # found self
                    here = self.context.first
                    it = ta		# boom now invalid?
                    faz = self
                    while ta > 0:
                        faz = faz.parent
                        ta = ta - 1
                    while here and it < len( bah ): # count them off to index
                        shr = bah[ len( bah ) - 1 - it ]
                        if here.context:
                            if here.context.name:
                                dis = here.context.name
                            else:
                                dis = '0'	# iter (fixme)
                        else:		# 0.
                            dis = '0'
                        if shr == dis:
                            bar = here
                        elif not here:
                            faz = None
                        else:
                            here = here.context.next
                            continue
                        here = bar.context.first
                        it = it + 1
                    break
                if itc == 1:
                    it = it + 1
            it = it - 1
        else:
            it = len( boom ) - 1
        print( 'ctp2: bah ', str( bah ), ' boom ', str( boom ) )
        print( ' bar ', str( bar ), ' faz ', str( faz ) )
        it = 0				# or what it was dropped to
        if not bar:
            bar = self			# first relevant act if param is one word.
        else:
            bar = faz
            sis = bar.tocx()
        tha = len( bah ) - 1		# 1 - 1
        while tha >= 0 and bar.context:
            print( 'ctp3: bah ', str( bah ), ' boom ', str( boom ) )
            print( ' sis ', str( bah ), ' faz ', str( boom ) )
            print( ' bar ', str( bar ), ' faz ', str( faz ) )
            string = bah[ tha ]
            if bar.context.first:	# should bah/place (param) be a subcontext, bar will be that.
                lem = bar.context.first	# can i?
            else:			# create '0'?
                break
            idx = 0
            while lem:
                print( 'if link: ', lem.id_mask )
                if bar.context.which( lem ) == string: # if the first self.element or any other element is the parameter
                    if not lem.context:
                        lem.clothe()
                    bar = lem		# good	# ado this???  it doesn't seem to separate elems
                    break
                if not lem.context: # ???
                    lem.clothe()
                lem = lem.context.next	# until string is found
                idx = idx + 1
            print( 'checking if link: ', bar.id_mask )
            if bar.id_mask == 4 and bar.to:
                # variables I want to use below: bah[ tha ], bar=self, lem.  no others needed from above.
                print( 'following link' )
                bar = bar.to
            if not lem:
                break
            tha = tha - 1		# this loop falls out with only one parameterized word.
        print( 'cxtoptr bar: ', bar.tocx() ) # was us, more recently utah.us
        print( 'tha: ', tha )
        if bar:				# all the way in as far as bah[ tha ], bar changes.
            while tha >= 0:		# for one parameter word, create and dub a new atom onto bar.
                if not bar.context:
                    bar.clothe()
                if not bar.context.first:
                    print( 'cx: ', bar.context.name, 'ins' )
                    bar = bar.context.ins( atom( bar, 1 ) )
                #bar = bar.context.ins_at( atom( bar, 1 ), bar.context.first )
                else:
                    print( 'cx: ', bar.context.name, 'ins_at' )
                    bar = bar.context.ins_at( bar.context.first, atom( bar, 1 ) )
                #print( 'ctp4: bar ', str( bar.tocx() ), ' bah ', str( bah ) )
                if bah[ tha ] != '0':		# fixme, renames 0.x; probably try attaching to the end of the list.
                    #if bar.context and bar.context.next: #and bar.context.next.context:
                    print( '!=0: ', bah[ tha ] )
                    if ( not bar.context ): #and ( ( not bar.context.next ) or ( not bar.context.next.context ) ):
                        bar.clothe() # error fixme
                    bar.context.dub( bah[ tha ] ) # new
                #bar.context.name = bah[ tha ]
                #break
                #else:
                #if( bar.parent.context.first != bar.parent.context.last ):
                #    None
                print( 'tha: ', tha )
                tha = tha - 1
                #break # None
            #print( 'cxtoptr: ', bar.context.name )
            print( 'cxtoptr: ', bar.tocx() )
            return bar # changed aug 2018 from None
        return None
    def lineup(self):
        sis = self.parent # is this actually self.parent.parent?  nope.
        la = line( sis, self.context )
        lb = sis.context.isol( self )		# am I not getting my data back?  aug 2018
        sis.context.ins( la )
        #if sis.context:
        #    sis.context.a = sis
        del self
        return la
    def linkup(self):
        sis = self.parent # is this actually self.parent.parent?  nope.
        la = link_( sis, self.context )
        lb = sis.context.isol( self )
        sis.context.ins( la ) # huh.  new
        #if sis.context:
        #    sis.context.a = sis
        del self
        #self = la
        return la
    #    if 0 and sis.context:
    #        #if sis.context.first == self:
    #        #    if not self.context:
    #        #        None
    #        #else:			# fixme, renames 0.x
    #        #    line.clothe()
    #        #    line.context.name = self.context.name
    #        #boom = sis.context.isol( self ) # bad
    #        #boom = self
    #        #sis.context.ins_by( boom, la ) # bad
    #        del self			# work?
    #    elif 0:
    #        ls = sis.first		# an atom
    #        while ls != self:
    #            ls = ls.next
    #        print( 'error: what points here?', ls )
    def tocx(self):
        leaf = None
        boom = None
        if self.parent:			# normal circumstances
            boom = self.parent.context
        if self.context:
            if self.context and boom:
                #if not leaf:
                print( '+:', boom.which( self ) )
                leaf = boom.which( self )
                if not leaf:		# fixed aug 2018
                    print( '/' )
                    leaf = self.context.name # us
                if not leaf:
                    leaf = str( boom.elem( self ) )
                    print( 'elem: ', str( leaf ) )
                #    return 'invalid'		# a further fix, aug 2018
            elif not boom:
                #print( '-' )
                leaf = self.context.name
                if not leaf:
                    leaf = '0'
            #else:
            #    leaf = boom.name
        else:
            if self.parent and leaf:
                leaf = leaf + '.' + boom.which( self )
            else:
                print( '/:', boom.which( self ) )
                leaf = boom.which( self )
        #print( 'a: ' + str( leaf ) );
        if not leaf:			# as sub node or( no name, no sublets )
            sir = boom.elem( self ) #+ 1 # aug 2018, not applied
            #if( boom.name ):
            #    leaf #leaf = boom.name	# ??? '0.' +
            #else:
            leaf = str( sir )
        if not boom:			# top
            return leaf
        while boom:
            #print( 'iter: ' + str( boom.elems() ) + ' ' + str( boom.name ) )
            if not boom.up:
                if boom.name:
                    leaf = leaf + '.' + boom.name
                else:
                    leaf = leaf + '.0'
            else:
                #print( '*' )
                if boom.name:
                    leaf = leaf + '.' + boom.name
                else:
                     leaf = leaf + '.0'
            node = boom.a
            print( 'tocx: ', leaf, boom.a.id_mask )
            boom = boom.up
            #if boom and boom.up:
            #    leaf = leaf + '.' + boom.up.which( boom.a )
        return leaf
    def ptrtocx(self, ptom):
        return None
#
# top = atom( None, 1 )
#chaff:
# top.context.ins( atom( top, 1 ) )
#            #leaf = self.context.name	# to define here
#            #if self.context.first:
#                #if boom and boom.up:
#                #    leaf = leaf + '.' + boom.up.which( boom.a )
#                #print( 'first' )
#                #else:
#                #if boom and boom.up and leaf:
#                #    print( 'scf: ' + boom.name )
#                #    print( 'sup: ' + boom.up.which( boom.a ) )
#                #    leaf = leaf + '.' + boom.up.which( boom.a )

class buffer:
    def __init__(self):
        self.text = bytearray( 20 )
#

class line(atom, buffer):
    def __init__( self, parent, c ):
        atom.__init__( self, parent, 2 )
        buffer.__init__( self )
        if c:
            self.context = c
            c.a = self			# good
            #self.clothe()
            #self.context.name = name
        #print( 'c: ', c )
        #print( 'sname: ', self.tocx() )
        #print( 'oname: ', parent.tocx() )
        #print( 'cx: ', self.context.name )
        #print( 'pcx: ', self.parent.context.name )
        #print( 'scx: ', self.context.name )
        self.length = 0
        self.size = 1
        self.owner = None
        self.rwx = 764
        self.color = 7
    def last(self):			# because line.h says
        if not self.context:
            return None
        return self.context.prev
    def next(self):
        if not self.context:
            return None
        return self.context.next
#

class link_(atom):
    def __init__(self, parent, c):
        atom.__init__(self, parent, 4)
        if c:
            self.context = c
            c.a = self
        self.to = ''			# atom
        #return self			# init should return None.
    def point(self, text):
        temp = self.to
        self.to = text			# please validate.
        if( temp ):
            del temp
#

#print( top.tocx() )
#print( top.context.first.tocx() )
#print( top.context.first.context.first.tocx() )
#print( top.context.first.context.first.context.first.context.next.tocx() )
