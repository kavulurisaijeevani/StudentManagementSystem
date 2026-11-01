
import { useState, useEffect } from 'react'
import './App.css'

function App() {

  const [students, setStudents] = useState([])

  // Form values
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [department, setDepartment] = useState('')

  // Search value
  const [search, setSearch] = useState('')

  // Editing information
  const [editingId, setEditingId] = useState(null)

  // Loading and messages
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [deletingId, setDeletingId] = useState(null)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  // Fetch students
  async function fetchStudents() {
    try {
      setError('')

      const response = await fetch(
        'http://127.0.0.1:8000/students'
      )

      if (!response.ok) {
        throw new Error('Unable to fetch student records')
      }

      const data = await response.json()
      setStudents(data)

    } catch (error) {
      setError(error.message)

    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStudents()
  }, [])

  // Validate form
  function validateForm() {

    if (!name.trim()) {
      return 'Student name cannot be empty.'
    }

    if (!email.trim()) {
      return 'Email address cannot be empty.'
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!emailPattern.test(email.trim())) {
      return 'Please enter a valid email address.'
    }

    if (!department.trim()) {
      return 'Department cannot be empty.'
    }

    return ''
  }

  // Edit student
  function handleEdit(student) {
    setEditingId(student.id)
    setName(student.name)
    setEmail(student.email)
    setDepartment(student.department || '')

    setMessage('')
    setError('')
  }

  // Clear form
  function handleCancel() {
    setEditingId(null)
    setName('')
    setEmail('')
    setDepartment('')
    setError('')
  }

  // Add or update student
  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setMessage('')

    const validationError = validateForm()

    if (validationError) {
      setError(validationError)
      return
    }

    setSubmitting(true)

    const studentData = {
      name: name.trim(),
      email: email.trim(),
      department: department.trim()
    }

    try {
      const url = editingId
        ? `http://127.0.0.1:8000/students/${editingId}`
        : 'http://127.0.0.1:8000/students'

      const method = editingId ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(studentData)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to save student details'
        )
      }

      const successMessage = editingId
        ? 'Student updated successfully!'
        : 'Student added successfully!'

      handleCancel()
      setMessage(successMessage)

      await fetchStudents()

    } catch (error) {
      setError(error.message)

    } finally {
      setSubmitting(false)
    }
  }

  // Delete student
  async function handleDelete(student) {

    const confirmed = window.confirm(
      `Are you sure you want to delete ${student.name}?`
    )

    if (!confirmed) return

    setError('')
    setMessage('')
    setDeletingId(student.id)

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/students/${student.id}`,
        { method: 'DELETE' }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to delete student'
        )
      }

      if (editingId === student.id) {
        handleCancel()
      }

      setMessage('Student deleted successfully!')

      await fetchStudents()

    } catch (error) {
      setError(error.message)

    } finally {
      setDeletingId(null)
    }
  }

  // Search students
  const filteredStudents = students.filter(student => {

    const searchText = search.toLowerCase().trim()

    return (
      String(student.student_code || '')
        .toLowerCase()
        .includes(searchText) ||

      student.name.toLowerCase().includes(searchText) ||

      student.email.toLowerCase().includes(searchText) ||

      (student.department || '')
        .toLowerCase()
        .includes(searchText)
    )
  })

  return (
    <div className="container">

      <h1>Student Management System</h1>

      {/* Add or Edit Form */}

      <div className="form-container">

        <h2>
          {editingId ? 'Edit Student' : 'Add New Student'}
        </h2>

        <form onSubmit={handleSubmit} noValidate>

          <input
            type="text"
            placeholder="Enter student name"
            value={name}
            onChange={event => {
              setName(event.target.value)
              setError('')
            }}
          />

          <input
            type="email"
            placeholder="Enter email address"
            value={email}
            onChange={event => {
              setEmail(event.target.value)
              setError('')
            }}
          />

          <input
            type="text"
            placeholder="Enter department"
            value={department}
            onChange={event => {
              setDepartment(event.target.value)
              setError('')
            }}
          />

          <button type="submit" disabled={submitting}>
            {submitting
              ? 'Saving...'
              : editingId
                ? 'Update Student'
                : 'Add Student'}
          </button>

          {editingId && (
            <button
              type="button"
              className="cancel-button"
              onClick={handleCancel}
            >
              Cancel
            </button>
          )}

        </form>
      </div>

      {/* Messages */}

      {message && (
        <p className="success-message">{message}</p>
      )}

      {error && (
        <p className="error-message">{error}</p>
      )}

      {/* Search Box */}

      <h2>Student Records</h2>

      <input
        className="search-input"
        type="text"
        placeholder="Search by Student ID, name, email or department..."
        value={search}
        onChange={event => setSearch(event.target.value)}
      />

      {loading && <p>Loading students...</p>}

      {!loading && (
        <>
          <p>
            Total matching students: {filteredStudents.length}
          </p>

          <table>

            <thead>
              <tr>
                <th>S.No.</th>
                <th>Student ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              {filteredStudents.length > 0 ? (

                filteredStudents.map((student, index) => (

                  <tr key={student.id}>

                    {/* Serial Number */}
                    <td>{index + 1}</td>

                    {/* Customized Student ID */}
                    <td>{student.student_code || 'Not assigned'}</td>

                    {/* Student Details */}
                    <td>{student.name}</td>
                    <td>{student.email}</td>
                    <td>{student.department}</td>

                    {/* Action Buttons */}
                    <td className="action-buttons">

                      <button
                        type="button"
                        className="edit-button"
                        onClick={() => handleEdit(student)}
                      >
                        Edit
                      </button>

                      <button
                        type="button"
                        className="delete-button"
                        disabled={deletingId !== null}
                        onClick={() => handleDelete(student)}
                      >
                        {deletingId === student.id
                          ? 'Deleting...'
                          : 'Delete'}
                      </button>

                    </td>

                  </tr>

                ))

              ) : (

                <tr>
                  <td colSpan="6">
                    No students found.
                  </td>
                </tr>

              )}

            </tbody>

          </table>
        </>
      )}

    </div>
  )
}

export default App
