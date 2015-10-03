#include <stdlib.h>
#include <stdio.h>
#include <string.h>

struct hashtable {
  int entries;
  int buckets;
  char ** keys;
  void ** values;
};

struct hashtable makeHashtable(int buckets) {
  struct hashtable ht;
  ht.buckets = buckets;
  ht.entries = 0;
  ht.keys = malloc(buckets*sizeof(char *));
  bzero(ht.keys, buckets*sizeof(char *));
  ht.values = malloc(buckets*sizeof(void *));
  return ht;
}

int deleteHashtable(struct hashtable ht) {
  free(ht.keys);
  free(ht.values);
  return 0;
}

float loadfactor(struct hashtable ht) {
  return ht.entries/(float)ht.buckets;
}

int hash(char * key) {
  int i;
  int hashval = 0;
  for (i = 0; i < strlen(key); i++) {
    hashval += key[i];
  }
  return hashval;
}

int put(struct hashtable * ht, char * key, void * value) {
  int hashval = hash(key) % ht->buckets;

  /* linear probing */
  while (ht->keys[hashval] != NULL) {
    hashval = (hashval + 1) % ht->buckets;
  }

  /* add to table and increment entry count */
  ht->keys[hashval] = key;
  ht->values[hashval] = value;
  ht->entries += 1;

  /* increase hashtable size if loadfactor too large */
  if (loadfactor(*ht) >= 0.7) {
    struct hashtable newHt = makeHashtable(ht->buckets*2);
    int i;
    for (i = 0; i < ht->buckets; i++) {
      if (ht->keys[i] != NULL) {
        put(&newHt, ht->keys[i], ht->values[i]);
      }
    }
    deleteHashtable(*ht);
    *ht = newHt;
  }

  return 0;
}

void * get(struct hashtable ht, char * key) {
  int hashval = hash(key) % ht.buckets;
  int probeval = hashval;

  /* linear probing */
  while (ht.keys[probeval] != NULL &&
         strcmp(ht.keys[probeval], key) != 0) {
    probeval = (probeval + 1) % ht.buckets;
    if (probeval == hashval) {
      return NULL;
    }
  }

  return ht.values[probeval];
}

void print(struct hashtable ht) {
  int i;
  for (i = 0; i < ht.buckets; i++) {
    printf("%d: <%s> <%s>\n", i, ht.keys[i], (char *) ht.values[i]);
  }
}

int main() {
  struct hashtable ht = makeHashtable(2);

  char * buf = NULL;
  char * cmd, * key, * value;
  size_t size = 0;
  do {
    free(buf);
    getline(&buf, &size, stdin);

    if (buf[strlen(buf)-1] == '\n') {
      buf[strlen(buf)-1] = '\0';
    }

    cmd = strsep(&buf, " ");
    key = strsep(&buf, " ");
    value = strsep(&buf, " ");

    if (strcmp(cmd, "put") == 0) {
      if (key == NULL || value == NULL) {
        printf("usage: put <key> <value>\n");
        continue;
      }
      put(&ht, key, value);
    } else if (strcmp(cmd, "get") == 0) {
      if (key == NULL) {
        printf("usage: get <key>");
        continue;
      }
      printf("%s\n", (char *) get(ht, key));
    } else if (strcmp(cmd, "info") == 0) {
      printf("loadfactor: %f, entries: %d, buckets: %d\n",
             loadfactor(ht), ht.entries, ht.buckets);
    } else if (strcmp(cmd, "print") == 0) {
      print(ht);
    } else if (strcmp(cmd, "q") == 0) {
      break;
    } else {
      printf("usage: [ put | get | info | q ]\n");
      continue;
    }
  } while (1);

  return 0;
}
