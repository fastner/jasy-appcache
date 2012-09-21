/* =============================================================================
 *
 * AppCache for Jasy - App cache supporting library
 *
 *
 * Copyright (C) 2012 Sebastian Fastner, Mainz, Germany
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */
 
(function(global) {

	var appCache = global.applicationCache;
	
	core.Module("appcache.AppCache", {
		/**
		 * {Boolean} Start application caching in browser, returns <code>false</code> if app cache is not supported.
		 */
		start : function(baseURL) {
			if (!!appCache) {
				var iframe = document.createElement("iframe");
				lowland.bom.Style.set(iframe, {
					position: "absolute",
					top: "-5000px",
					width: "1px",
					height: "1px"
				});

				var src = baseURL ? baseURL : '';
				src += 'index-' + jasy.Env.CHECKSUM + '.html';
				iframe.src = src;
				
				document.body.appendChild(iframe);
				
				return true;
			} else {
				return false;
			}
		},
		
		/**
		 * {String|null} Return application cache status or null if not supported
		 */
		status : function() {
			if (!appCache) {
				return null;
			}
			
			switch (appCache.status) {
				case appCache.UNCACHED: // UNCACHED == 0
					return 'UNCACHED';
					break;
				case appCache.IDLE: // IDLE == 1
					return 'IDLE';
					break;
				case appCache.CHECKING: // CHECKING == 2
					return 'CHECKING';
					break;
				case appCache.DOWNLOADING: // DOWNLOADING == 3
					return 'DOWNLOADING';
					break;
				case appCache.UPDATEREADY:  // UPDATEREADY == 4
					return 'UPDATEREADY';
					break;
				case appCache.OBSOLETE: // OBSOLETE == 5
					return 'OBSOLETE';
					break;
				default:
					return 'UKNOWN CACHE STATUS';
					break;
			};
		}
	});

})(this);
