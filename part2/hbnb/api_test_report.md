# API Test Report

## Test: Create a new user

**Result:** ✅ Passed

**Expected Status:** 201

**Actual Status:** 201

**Command:**
```bash
curl -s -X POST "http://localhost:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Output:**
```json
{
    "id": "518ee7a6-2cb0-40be-9632-984b76bce62e",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

---

## Test: Create a user with existing email

**Result:** ✅ Passed

**Expected Status:** 409

**Actual Status:** 409

**Command:**
```bash
curl -s -X POST "http://localhost:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "Jane", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Output:**
```json
{
    "error": "Email already registered"
}
```

---

## Test: Get all users

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/users/"
```

**Output:**
```json
[
    {
        "id": "518ee7a6-2cb0-40be-9632-984b76bce62e",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
]
```

---

## Test: Get a specific user

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/users/"
```

**Output:**
```json
[
    {
        "id": "518ee7a6-2cb0-40be-9632-984b76bce62e",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
]
```

---

## Test: Update a user

**Result:** ❌ Failed

**Expected Status:** 200

**Actual Status:** 405

**Command:**
```bash
curl -s -X PUT "http://localhost:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Smith", "email": "john.smith@example.com"}'
```

**Output:**
```json
{
    "message": "The method is not allowed for the requested URL."
}
```

---

## Test: Create a new place

**Result:** ❌ Failed

**Expected Status:** 201

**Actual Status:** 500

**Command:**
```bash
curl -s -X POST "http://localhost:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"name": "Cozy Apartment", "description": "A lovely place to stay", "number_rooms": 2, "number_bathrooms": 1, "max_guest": 4, "price_by_night": 100, "latitude": 40.7128, "longitude": -74.0060, "user_id": ""}'
```

**Output:**
```json
<!doctype html>
<html lang=en>
  <head>
    <title>KeyError: &#39;owner_id&#39;
 // Werkzeug Debugger</title>
    <link rel="stylesheet" href="?__debugger__=yes&amp;cmd=resource&amp;f=style.css">
    <link rel="shortcut icon"
        href="?__debugger__=yes&amp;cmd=resource&amp;f=console.png">
    <script src="?__debugger__=yes&amp;cmd=resource&amp;f=debugger.js"></script>
    <script>
      var CONSOLE_MODE = false,
          EVALEX = true,
          EVALEX_TRUSTED = false,
          SECRET = "lekmedEdy4UesrMmyrzz";
    </script>
  </head>
  <body style="background-color: #fff">
    <div class="debugger">
<h1>KeyError</h1>
<div class="detail">
  <p class="errormsg">KeyError: &#39;owner_id&#39;
</p>
</div>
<h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
<div class="traceback">
  <h3></h3>
  <ul><li><div class="frame" id="frame-140619071391200">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py"</cite>,
      line <em class="line">1536</em>,
      in <code class="function">__call__</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">    </span>) -&gt; cabc.Iterable[bytes]:</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;The WSGI server calls the Flask application object as the</pre>
<pre class="line before"><span class="ws">        </span>WSGI application. This calls :meth:`wsgi_app`, which can be</pre>
<pre class="line before"><span class="ws">        </span>wrapped to apply middleware.</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line current"><span class="ws">        </span>return self.wsgi_app(environ, start_response)
<span class="ws">        </span>       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre></div>
</div>

<li><div class="frame" id="frame-140619071392352">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py"</cite>,
      line <em class="line">1514</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line before"><span class="ws">                </span>response = self.full_dispatch_request()</pre>
<pre class="line before"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line before"><span class="ws">                </span>error = e</pre>
<pre class="line current"><span class="ws">                </span>response = self.handle_exception(e)
<span class="ws">                </span>           ^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre>
<pre class="line after"><span class="ws">                </span>raise</pre>
<pre class="line after"><span class="ws">            </span>return response(environ, start_response)</pre>
<pre class="line after"><span class="ws">        </span>finally:</pre></div>
</div>

<li><div class="frame" id="frame-140619071392496">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py"</cite>,
      line <em class="line">671</em>,
      in <code class="function">error_router</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>if self._has_fr_route():</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>return self.handle_error(e)</pre>
<pre class="line before"><span class="ws">            </span>except Exception as f:</pre>
<pre class="line current"><span class="ws">                </span>return original_handler(f)
<span class="ws">                </span>       ^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">        </span>return original_handler(e)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _propagate_exceptions(self):</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line after"><span class="ws">        </span>Returns the value of the ``PROPAGATE_EXCEPTIONS`` configuration</pre></div>
</div>

<li><div class="frame" id="frame-140619071394512">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py"</cite>,
      line <em class="line">669</em>,
      in <code class="function">error_router</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>:param function original_handler: the original Flask error handler for the app</pre>
<pre class="line before"><span class="ws">        </span>:param Exception e: the exception raised while handling the request</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>if self._has_fr_route():</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>return self.handle_error(e)
<span class="ws">                </span>       ^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">            </span>except Exception as f:</pre>
<pre class="line after"><span class="ws">                </span>return original_handler(f)</pre>
<pre class="line after"><span class="ws">        </span>return original_handler(e)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _propagate_exceptions(self):</pre></div>
</div>

<li><div class="frame" id="frame-140619071394656">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py"</cite>,
      line <em class="line">1511</em>,
      in <code class="function">wsgi_app</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>ctx = self.request_context(environ)</pre>
<pre class="line before"><span class="ws">        </span>error: BaseException | None = None</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>ctx.push()</pre>
<pre class="line current"><span class="ws">                </span>response = self.full_dispatch_request()
<span class="ws">                </span>           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">            </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">                </span>error = e</pre>
<pre class="line after"><span class="ws">                </span>response = self.handle_exception(e)</pre>
<pre class="line after"><span class="ws">            </span>except:  # noqa: B001</pre>
<pre class="line after"><span class="ws">                </span>error = sys.exc_info()[1]</pre></div>
</div>

<li><div class="frame" id="frame-140619071394800">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py"</cite>,
      line <em class="line">919</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line before"><span class="ws">                </span>rv = self.dispatch_request()</pre>
<pre class="line before"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line current"><span class="ws">            </span>rv = self.handle_user_exception(e)
<span class="ws">            </span>     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre>
<pre class="line after"><span class="ws">        </span>self,</pre>
<pre class="line after"><span class="ws">        </span>rv: ft.ResponseReturnValue | HTTPException,</pre></div>
</div>

<li><div class="frame" id="frame-140619071394944">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py"</cite>,
      line <em class="line">671</em>,
      in <code class="function">error_router</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>if self._has_fr_route():</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line before"><span class="ws">                </span>return self.handle_error(e)</pre>
<pre class="line before"><span class="ws">            </span>except Exception as f:</pre>
<pre class="line current"><span class="ws">                </span>return original_handler(f)
<span class="ws">                </span>       ^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">        </span>return original_handler(e)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _propagate_exceptions(self):</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line after"><span class="ws">        </span>Returns the value of the ``PROPAGATE_EXCEPTIONS`` configuration</pre></div>
</div>

<li><div class="frame" id="frame-140619071395088">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py"</cite>,
      line <em class="line">669</em>,
      in <code class="function">error_router</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>:param function original_handler: the original Flask error handler for the app</pre>
<pre class="line before"><span class="ws">        </span>:param Exception e: the exception raised while handling the request</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>if self._has_fr_route():</pre>
<pre class="line before"><span class="ws">            </span>try:</pre>
<pre class="line current"><span class="ws">                </span>return self.handle_error(e)
<span class="ws">                </span>       ^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">            </span>except Exception as f:</pre>
<pre class="line after"><span class="ws">                </span>return original_handler(f)</pre>
<pre class="line after"><span class="ws">        </span>return original_handler(e)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def _propagate_exceptions(self):</pre></div>
</div>

<li><div class="frame" id="frame-140619071395232">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py"</cite>,
      line <em class="line">917</em>,
      in <code class="function">full_dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line before"><span class="ws">            </span>request_started.send(self, _async_wrapper=self.ensure_sync)</pre>
<pre class="line before"><span class="ws">            </span>rv = self.preprocess_request()</pre>
<pre class="line before"><span class="ws">            </span>if rv is None:</pre>
<pre class="line current"><span class="ws">                </span>rv = self.dispatch_request()
<span class="ws">                </span>     ^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">        </span>except Exception as e:</pre>
<pre class="line after"><span class="ws">            </span>rv = self.handle_user_exception(e)</pre>
<pre class="line after"><span class="ws">        </span>return self.finalize_request(rv)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def finalize_request(</pre></div>
</div>

<li><div class="frame" id="frame-140619071395376">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py"</cite>,
      line <em class="line">902</em>,
      in <code class="function">dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">            </span>and req.method == &#34;OPTIONS&#34;</pre>
<pre class="line before"><span class="ws">        </span>):</pre>
<pre class="line before"><span class="ws">            </span>return self.make_default_options_response()</pre>
<pre class="line before"><span class="ws">        </span># otherwise dispatch to the handler for that endpoint</pre>
<pre class="line before"><span class="ws">        </span>view_args: dict[str, t.Any] = req.view_args  # type: ignore[assignment]</pre>
<pre class="line current"><span class="ws">        </span>return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
<span class="ws">        </span>       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">    </span>def full_dispatch_request(self) -&gt; Response:</pre>
<pre class="line after"><span class="ws">        </span>&#34;&#34;&#34;Dispatches the request and on top of that performs request</pre>
<pre class="line after"><span class="ws">        </span>pre and postprocessing as well as HTTP exception catching and</pre>
<pre class="line after"><span class="ws">        </span>error handling.</pre></div>
</div>

<li><div class="frame" id="frame-140619071395520">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py"</cite>,
      line <em class="line">402</em>,
      in <code class="function">wrapper</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>:param resource: The resource as a flask view function</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>@wraps(resource)</pre>
<pre class="line before"><span class="ws">        </span>def wrapper(*args, **kwargs):</pre>
<pre class="line current"><span class="ws">            </span>resp = resource(*args, **kwargs)
<span class="ws">            </span>       ^^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">            </span>if isinstance(resp, BaseResponse):</pre>
<pre class="line after"><span class="ws">                </span>return resp</pre>
<pre class="line after"><span class="ws">            </span>data, code, headers = unpack(resp)</pre>
<pre class="line after"><span class="ws">            </span>return self.make_response(data, code, headers=headers)</pre>
<pre class="line after"><span class="ws"></span> </pre></div>
</div>

<li><div class="frame" id="frame-140619071395664">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/views.py"</cite>,
      line <em class="line">110</em>,
      in <code class="function">view</code></h4>
  <div class="source library"><pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">            </span>def view(**kwargs: t.Any) -&gt; ft.ResponseReturnValue:</pre>
<pre class="line before"><span class="ws">                </span>self = view.view_class(  # type: ignore[attr-defined]</pre>
<pre class="line before"><span class="ws">                    </span>*class_args, **class_kwargs</pre>
<pre class="line before"><span class="ws">                </span>)</pre>
<pre class="line current"><span class="ws">                </span>return current_app.ensure_sync(self.dispatch_request)(**kwargs)  # type: ignore[no-any-return]
<span class="ws">                </span>       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>else:</pre>
<pre class="line after"><span class="ws">            </span>self = cls(*class_args, **class_kwargs)  # pyright: ignore</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">            </span>def view(**kwargs: t.Any) -&gt; ft.ResponseReturnValue:</pre></div>
</div>

<li><div class="frame" id="frame-140619071395808">
  <h4>File <cite class="filename">"/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/resource.py"</cite>,
      line <em class="line">41</em>,
      in <code class="function">dispatch_request</code></h4>
  <div class="source library"><pre class="line before"><span class="ws">        </span>for decorator in self.method_decorators:</pre>
<pre class="line before"><span class="ws">            </span>meth = decorator(meth)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">        </span>self.validate_payload(meth)</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line current"><span class="ws">        </span>resp = meth(*args, **kwargs)
<span class="ws">        </span>       ^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>if isinstance(resp, BaseResponse):</pre>
<pre class="line after"><span class="ws">            </span>return resp</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>representations = self.representations or {}</pre></div>
</div>

<li><div class="frame" id="frame-140619071395952">
  <h4>File <cite class="filename">"/home/jbn/holbertonschool-hbnb/part2/hbnb/app/api/v1/places.py"</cite>,
      line <em class="line">38</em>,
      in <code class="function">post</code></h4>
  <div class="source "><pre class="line before"><span class="ws">    </span>@api.response(201, &#39;Place successfully created&#39;)</pre>
<pre class="line before"><span class="ws">    </span>@api.response(400, &#39;Invalid input data&#39;)</pre>
<pre class="line before"><span class="ws">    </span>def post(self):</pre>
<pre class="line before"><span class="ws">        </span>&#34;&#34;&#34;Register a new place&#34;&#34;&#34;</pre>
<pre class="line before"><span class="ws">        </span>try:</pre>
<pre class="line current"><span class="ws">            </span>new_place = facade.create_place(api.payload)
<span class="ws">            </span>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">            </span>return {</pre>
<pre class="line after"><span class="ws">                </span>&#39;id&#39;: new_place.id,</pre>
<pre class="line after"><span class="ws">                </span>&#39;title&#39;: new_place.title,</pre>
<pre class="line after"><span class="ws">                </span>&#39;description&#39;: new_place.description,</pre>
<pre class="line after"><span class="ws">                </span>&#39;price&#39;: new_place.price,</pre></div>
</div>

<li><div class="frame" id="frame-140619071396240">
  <h4>File <cite class="filename">"/home/jbn/holbertonschool-hbnb/part2/hbnb/app/services/facade.py"</cite>,
      line <em class="line">59</em>,
      in <code class="function">create_place</code></h4>
  <div class="source "><pre class="line before"><span class="ws">            </span>return amenity</pre>
<pre class="line before"><span class="ws">        </span>return None</pre>
<pre class="line before"><span class="ws"></span> </pre>
<pre class="line before"><span class="ws">    </span># Place-related methods</pre>
<pre class="line before"><span class="ws">    </span>def create_place(self, place_data):</pre>
<pre class="line current"><span class="ws">        </span>owner = self.get_user(place_data[&#39;owner_id&#39;])
<span class="ws">        </span>                      ^^^^^^^^^^^^^^^^^^^^^^</pre>
<pre class="line after"><span class="ws">        </span>if not owner:</pre>
<pre class="line after"><span class="ws">            </span>raise ValueError(&#34;Owner not found&#34;)</pre>
<pre class="line after"><span class="ws"></span> </pre>
<pre class="line after"><span class="ws">        </span>amenities = []</pre>
<pre class="line after"><span class="ws">        </span>for amenity_id in place_data.get(&#39;amenities&#39;, []):</pre></div>
</div>
</ul>
  <blockquote>KeyError: &#39;owner_id&#39;
</blockquote>
</div>

<div class="plain">
    <p>
      This is the Copy/Paste friendly version of the traceback.
    </p>
    <textarea cols="50" rows="10" name="code" readonly>Traceback (most recent call last):
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py&#34;, line 1536, in __call__
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py&#34;, line 1514, in wsgi_app
    response = self.handle_exception(e)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py&#34;, line 671, in error_router
    return original_handler(f)
           ^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py&#34;, line 669, in error_router
    return self.handle_error(e)
           ^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py&#34;, line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py&#34;, line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py&#34;, line 671, in error_router
    return original_handler(f)
           ^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py&#34;, line 669, in error_router
    return self.handle_error(e)
           ^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py&#34;, line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py&#34;, line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py&#34;, line 402, in wrapper
    resp = resource(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/views.py&#34;, line 110, in view
    return current_app.ensure_sync(self.dispatch_request)(**kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/resource.py&#34;, line 41, in dispatch_request
    resp = meth(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/holbertonschool-hbnb/part2/hbnb/app/api/v1/places.py&#34;, line 38, in post
    new_place = facade.create_place(api.payload)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/home/jbn/holbertonschool-hbnb/part2/hbnb/app/services/facade.py&#34;, line 59, in create_place
    owner = self.get_user(place_data[&#39;owner_id&#39;])
                          ^^^^^^^^^^^^^^^^^^^^^^^
KeyError: &#39;owner_id&#39;
</textarea>
</div>
<div class="explanation">
  The debugger caught an exception in your WSGI application.  You can now
  look at the traceback which led to the error.  <span class="nojavascript">
  If you enable JavaScript you can also use additional features such as code
  execution (if the evalex feature is enabled), automatic pasting of the
  exceptions and much more.</span>
</div>
      <div class="footer">
        Brought to you by <strong class="arthur">DON'T PANIC</strong>, your
        friendly Werkzeug powered traceback interpreter.
      </div>
    </div>

    <div class="pin-prompt">
      <div class="inner">
        <h3>Console Locked</h3>
        <p>
          The console is locked and needs to be unlocked by entering the PIN.
          You can find the PIN printed out on the standard output of your
          shell that runs the server.
        <form>
          <p>PIN:
            <input type=text name=pin size=14>
            <input type=submit name=btn value="Confirm Pin">
        </form>
      </div>
    </div>
  </body>
</html>

<!--

Traceback (most recent call last):
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py", line 671, in error_router
    return original_handler(f)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py", line 669, in error_router
    return self.handle_error(e)
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py", line 671, in error_router
    return original_handler(f)
           ^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py", line 669, in error_router
    return self.handle_error(e)
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/api.py", line 402, in wrapper
    resp = resource(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask/views.py", line 110, in view
    return current_app.ensure_sync(self.dispatch_request)(**kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/PROJETS/Hbnb_perso/OMG/venv/lib/python3.12/site-packages/flask_restx/resource.py", line 41, in dispatch_request
    resp = meth(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/holbertonschool-hbnb/part2/hbnb/app/api/v1/places.py", line 38, in post
    new_place = facade.create_place(api.payload)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jbn/holbertonschool-hbnb/part2/hbnb/app/services/facade.py", line 59, in create_place
    owner = self.get_user(place_data['owner_id'])
                          ^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'owner_id'


-->
```

---

## Test: Get all places

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/places/"
```

**Output:**
```json
[]
```

---

## Test: Get a specific place

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/places/"
```

**Output:**
```json
[]
```

---

## Test: Update a place

**Result:** ❌ Failed

**Expected Status:** 200

**Actual Status:** 405

**Command:**
```bash
curl -s -X PUT "http://localhost:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"name": "Luxurious Apartment", "price_by_night": 150}'
```

**Output:**
```json
{
    "message": "The method is not allowed for the requested URL."
}
```

---

## Test: Create a new amenity

**Result:** ✅ Passed

**Expected Status:** 201

**Actual Status:** 201

**Command:**
```bash
curl -s -X POST "http://localhost:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}'
```

**Output:**
```json
{
    "id": "83804491-cc1d-46c9-a1f9-6055265b39e7",
    "name": "Wi-Fi"
}
```

---

## Test: Get all amenities

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/amenities/"
```

**Output:**
```json
[
    {
        "id": "83804491-cc1d-46c9-a1f9-6055265b39e7",
        "name": "Wi-Fi"
    }
]
```

---

## Test: Get a specific amenity

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/amenities/"
```

**Output:**
```json
[
    {
        "id": "83804491-cc1d-46c9-a1f9-6055265b39e7",
        "name": "Wi-Fi"
    }
]
```

---

## Test: Update an amenity

**Result:** ❌ Failed

**Expected Status:** 200

**Actual Status:** 405

**Command:**
```bash
curl -s -X PUT "http://localhost:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{"name": "High-speed Wi-Fi"}'
```

**Output:**
```json
{
    "message": "The method is not allowed for the requested URL."
}
```

---

## Test: Create a new review

**Result:** ❌ Failed

**Expected Status:** 201

**Actual Status:** 400

**Command:**
```bash
curl -s -X POST "http://localhost:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{"text": "Great place to stay!", "rating": 5, "user_id": "", "place_id": ""}'
```

**Output:**
```json
{
    "error": "User or Place not found"
}
```

---

## Test: Get all reviews

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/reviews/"
```

**Output:**
```json
[]
```

---

## Test: Get a specific review

**Result:** ✅ Passed

**Expected Status:** 200

**Actual Status:** 200

**Command:**
```bash
curl -s -X GET "http://localhost:5000/api/v1/reviews/"
```

**Output:**
```json
[]
```

---

## Test: Update a review

**Result:** ❌ Failed

**Expected Status:** 200

**Actual Status:** 405

**Command:**
```bash
curl -s -X PUT "http://localhost:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{"text": "Amazing place, highly recommended!", "rating": 5}'
```

**Output:**
```json
{
    "message": "The method is not allowed for the requested URL."
}
```

---

# Test Summary

Total tests: 17
Passed tests: 11
Failed tests: 6

