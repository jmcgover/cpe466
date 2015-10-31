include ../../common.mk

LDLIBS := $(addprefix ../../lib/, $(PAGERANK_LIBS) $(EXTRA_LIBS))

LDLIBS_GROUP := $(LDLIBS)

$(BIN): $(LDLIBS) $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS) $(LDLIBS_GROUP)

%.a:
	$(MAKE) -C $(dir $@)
