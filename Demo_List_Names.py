__author__ = '143740'

__author__ = '143740'

sum_dict_names = {
    'F25-54': ['F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'F50-54'],
    'P25-54': ['F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'F50-54', 'M25-29', 'M30-34', 'M35-39', 'M40-44',
               'M45-49', 'M50-54'],
    'M25-54': ['M25-29', 'M30-34', 'M35-39', 'M40-44', 'M45-49', 'M50-54'],
    'F18-49': ['F18-20', 'F21-24', 'F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49'],
    'M18-49': ['M18-20', 'M21-24', 'M25-29', 'M30-34', 'M35-39', 'M40-44', 'M45-49'],
    'P18-49': ['F18-20', 'F21-24', 'F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'M18-20', 'M21-24', 'M25-29',
               'M30-34', 'M35-39', 'M40-44', 'M45-49'],
    'F25-49': ['F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49'],
    'P25-49': ['F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'M25-29', 'M30-34', 'M35-39', 'M40-44', 'M45-49'],
    'F35-54': ['F35-39', 'F40-44', 'F45-49', 'F50-54'],
    'P35-54': ['F35-39', 'F40-44', 'F45-49', 'F50-54', 'M35-39', 'M40-44', 'M45-49', 'M50-54'],
    'P25-64': ['F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'F50-54', 'F55-64', 'M25-29', 'M30-34', 'M35-39',
               'M40-44', 'M45-49', 'M50-54', 'M55-64'],
    'F35-64': ['F35-39', 'F40-44', 'F45-49', 'F50-54', 'F55-64'],
    'M35-64': ['M35-39', 'M40-44', 'M45-49', 'M50-54', 'M55-64'],
    'P35-64': ['F35-39', 'F40-44', 'F45-49', 'F50-54', 'F55-64', 'M35-39', 'M40-44', 'M45-49', 'M50-54', 'M55-64'],
    'F25+': ['F35-39', 'F40-44', 'F45-49', 'F50-54', 'F55-64', 'F65+'],
    'P35+': ['M35-39', 'M40-44', 'M45-49', 'M50-54', 'M55-64', 'M65+'],
    'F50+': ['F50-54', 'F55-64', 'F65+'],
    'F55+': ['F55-64', 'F65+'],
    'M25-34': ['M25-29', 'M30-34'],
    'F50-64': ['F50-54', 'F55-64'],
    'P45+': ['F45-49', 'F50-54', 'F55-64', 'F65+', 'M45-49', 'M50-54', 'M55-64', 'M65+'],
    'P21-49': ['F21-24', 'F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'M21-24', 'M25-29', 'M30-34', 'M35-39',
               'M40-44', 'M45-49'],
    'M21-34': ['M21-24', 'M25-29', 'M30-34'],
    'P21-34': ['F21-24', 'F25-29', 'F30-34', 'M21-24', 'M25-29', 'M30-34'],
    'HH': ['M2-5', 'M6-8', 'M9-11', 'M12-14', 'M15-17', 'M18-20', 'M21-24', 'M25-29', 'M30-34', 'M35-39', 'M40-44',
           'M45-49', 'M50-54', 'M55-64', 'M65+', 'F2-5', 'F6-8', 'F9-11', 'F12-14', 'F15-17', 'F18-20', 'F21-24',
           'F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'F50-54', 'F55-64', 'F65+'],
    'M25-49': ['M25-29', 'M30-34', 'M35-39', 'M40-44', 'M45-49']
}


# M2-5,M6-8,M9-11,M12-14,M15-17,M18-20,M21-24,M25-29,M30-34,M35-39,M40-44,M45-49,M50-54,M55-64,M65+
# F2-5,F6-8,F9-11,F12-14,F15-17,F18-20,F21-24,F25-29,F30-34,F35-39,F40-44,F45-49,F50-54,F55-64,F65+


# 37	F25-54 # 55	P25-54 # 214	HH # 215	M25-54 # 216	F18-49 # 217	P18-49 # 218	M18-49
# 219	F25-49 # 220	P25-49 # 221	M25-49 # 222	F35-49 # 223	P35-49 # 224	M35-49 # 225	F35-54
# 226	P35-54 # 227	M35-54 # 228	F25-64 # 229	P25-64 # 230	M25-64 # 231	F35-64 # 232	P35-64
# 233	M35-64 # 234	P18-34 # 235	F18-34 # 236	M18-34 # 237	F18+ # 238	P18+ # 239	M18+ # 240	F25+
# 241	P25+ # 242	M25+ # 243	F35+ # 244	P35+ # 245	M35+ # 246	F50+ # 247	P50+ # 248	M50+ # 249	F55+
# 250	P55+ # 251	M55+ # 252	M35-44 # 253	M25-34 # 254	P12-17 # 255	P18-24 # 256	P25-34
# 257	P35-44 # 258	P50-54 # 259	P65+ # 260	P2-11 # 261	P18-54 # 262	F18-54 # 263	M18-54
# 264	F35-44 # 265	P45-54 # 266	P18-64 # 267	F45+ # 268	P50-64 # 269	F50-64 # 270	P12-34
# 271	F45-64 # 272	M45-64 # 273	P45-64 # 275	F12-17 # 276	P6-11 # 277	P15-17 # 278	F15-17
# 279	F25-34 # 280	M18-24 # 281	F18-24 # 282	P12-24 # 283	F12-24 # 284	P25-44 # 285	F18-64
# 286	F65+ # 287	M2-14 # 288	M15-17 # 289	M18-20 # 290	M21-24 # 291	M25-29 # 292	M30-34
# 293	M35-39 # 294	M40-44 # 295	M45-49 # 296	M50-54 # 297	M55-64 # 298	M65+ # 299	F12-14
# 300	F18-20 # 301	F21-24 # 302	F25-29 # 303	F30-34 # 304	F35-39 # 305	F40-44 # 306	F45-49
# 307	F50-54 # 308	F55-64 # 309	M12-17 # 310	M12-34 # 311	M18-64 # 312	M25-44 # 313	M45+
# 314	M45-54 # 315	M50-64 # 316	F12-34 # 317	F25-44 # 318	F45-54 # 319	P45+ # 320	P55-64
# 322	P21-49 # 344	M12-24 # 345	M21-34 # 358	P9-14 # 362	P2+ # 363	F12-49 # 364	P12-49
# 365	M21-29 # 366	M21+ # 367	P21+ # 368	F21-34 # 369	F2-11 # 370	F6-11 # 371	F9-14 # 372	M12-49
# 373	M2-11 # 374	M6-11 # 375	M9-14 # 376	P21-34 # 377	F9-17 # 378	M21-49 # 379	P6-14 # 380	P21-44
# 381	M21-54 # 382	P18-44 # 383	F18-44 # 384	P21-24 # 385	P6-17 # 386	P30-39 # 387	P2-5
# 388	F21-49 # 389	F21-29 # 390	F30-54 # 391	P12-54 # 392	P40+ # 393	M18-44

