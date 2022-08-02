#!/usr/bin/python

import os.path
import re
import sys
import tempfile

def main(): # pragma: no cover
    commit_file_name = sys.argv[1]
    if CommitFileIsValid(commit_file_name):
        sys.exit(0)
    tmp_dir = tempfile.mkdtemp()
    rejected_file_name = os.path.join(tmp_dir, 'commit_msg')
    with open(commit_file_name, 'rb') as src, open(rejected_file_name, 'wb') as dst:
        while True:
            buffer_size = 2**20
            if copy_buffer := src.read(buffer_size):
                dst.write(copy_buffer)
            else:
                break
    print(f"Commit message saved in {rejected_file_name}")
    print("Fix the commit and try again with:")
    print(f"git commit -F {rejected_file_name}")
    print("Aborting Commit.")
    sys.exit(1)


def CommitFileIsValid(commit_file_name):
    with open(commit_file_name) as commit_file:

        subject_line = commit_file.readline()
        if not SubjectIsValid(subject_line):
            print("Subject: '" + subject_line.strip() + "'")
            print("Subject is not formatted correctly.  See .gitmessage.")
            return False

        label = LabelFromSubject(subject_line)
        if not LabelIsValid(label):
            print(f"Label for subject ({label}) is not valid  See .gitmessage.")
            return False

        blank_line = commit_file.readline()
        if not LineIsBlank(blank_line):
            print(f"'{blank_line}'")
            print("Separate the subject from the body with a blank line.  "
                  + "See .gitmessage.")
            return False

        for line in commit_file:
            if not LineLengthIsValid(line):
                print(
                    (
                        (
                            f"'{line}'"
                            + "Lines in body text should be 72 characters or less.  "
                        )
                        + "See .gitmessage"
                    )
                )

                return False
    return True


def SubjectIsValid(subject):
    subject = subject.strip()
    if SubjectIsBlank(subject):
        return False

    if SubjectIsMerge(subject):
        return True

    return (
        bool(SubjectLengthIsValid(subject))
        if SubjectHasLabel(subject)
        else False
    )


def SubjectIsBlank(subject):
    if not subject:
        print('Subject line is empty.')
        return True
    return False


def SubjectIsMerge(subject):
    return bool(
        (
            subject.startswith('Merge pull')
            or subject.startswith('Merge branch')
        )
    )


def SubjectHasLabel(subject):
    label_format = re.compile(r"[a-zA-Z][a-z]*:")
    if not label_format.match(subject):
        print('Subject should be in the form of "<label>: <Subject>".')
        return False
    return True


def SubjectLengthIsValid(subject):
    soft_limit = 50
    hard_limit = soft_limit + 10
    if len(subject) > hard_limit:
        print(f"Subject line must be less than {soft_limit} characters.")
        return False
    return True


def SubjectIsCapitalized(subject):
    line_format = re.compile(r"[a-zA-Z][a-z]*:\s[A-Z]")
    if not line_format.match(subject):
        print('The subject should be capitalized.')
        return False
    return True


def LabelFromSubject(subject):
    label = subject.split(":")[0]
    label = label.split(" ")[0]
    return label


def LabelIsValid(label):
    valid_labels = {
        'chore',
        'docs',
        'feat',
        'fix',
        'merge',
        'refactor',
        'revert',
        'style',
        'test',
        'tool',
    }

    return label.lower() in valid_labels


def LineIsBlank(text_line):
    if text_line.startswith('#'):
        return True
    return not (stripped_text := text_line.strip())


def LineLengthIsValid(text_line):
    if LineIsBlank(text_line):
        return True
    stripped_text = text_line.strip()
    hard_limit = 80
    if len(stripped_text) > hard_limit:
        soft_limit = 72
        print(f"{stripped_text}:Text line must be less than {soft_limit} characters.")
        return False
    return True


if __name__ == "__main__":  # pragma: no cover
    main()
